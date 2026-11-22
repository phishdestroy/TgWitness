import argparse
import asyncio
import errno
import hashlib
import io
import json
import logging
import secrets
import shutil
import time
from contextlib import asynccontextmanager
from functools import partial
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .collector import Collector, WitnessClient
from .account_export import AccountExport, file_sha
from .evidence import BundleSizeLimit, export_file
from .middleware import KEEP_ALIVE_SECONDS, RequestLimit
from .monitoring import capture_settings, normalize_capture
from .export_preflight import preview_capture
from .failures import describe
from . import export_budget
from .provenance import run_receipt
from .sealed_crypto import recipient_id
from .sealed_selection import Selection, selection_hash
from .sealed_parts import EncryptedParts, PART_BYTES, SEALED_RESULT
from .security import InstanceLock, Vault, private_write
from .store import Store, canonical
from .workers import complete_in_thread

STATIC = Path(__file__).with_name("static")
# Built into the sealed image from the pinned upstream archive; checked again against the pinned SHA-256 before loading.
IMAGE_MODULES = Path("/usr/share/tgwitness-modules")
TERMINAL = {"sealed", "cancelled", "failed"}
# The account export travels inside the sealed evidence archive under this name; its own verify commands point at it.
ACCOUNT_MEMBER = "account-export.zip"


class StrictBody(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Login(StrictBody):
    api_id: int | None = Field(default=None, strict=True, gt=0, le=2147483647)
    api_hash: str | None = Field(default=None, pattern=r"^[a-fA-F0-9]{32}$")

    @field_validator("api_id", "api_hash", mode="before")
    @classmethod
    def empty_field(cls, value):
        return None if isinstance(value, str) and not value.strip() else value

    @model_validator(mode="after")
    def complete_pair(self):
        if (self.api_id is None) != (self.api_hash is None):
            raise ValueError("Supply both API credentials or leave both empty")
        return self


class Phone(Login):
    phone: str = Field(pattern=r"^\+[0-9]{7,16}$")


class Code(StrictBody):
    code: str = Field(min_length=3, max_length=12, pattern=r"^[0-9 -]+$")


class Password(StrictBody):
    password: str = Field(min_length=1, max_length=512)


class Session:
    def __init__(self, root, output, config, client_factory):
        self.root, self.output, self.config = Path(root), Path(output), config

        if self.root.exists() and any(self.root.iterdir()):
            raise ValueError("A sealed capture requires a new empty data directory")
        if self.output.exists() and any(self.output.iterdir()):
            raise ValueError("A sealed capture requires a new empty output directory")
        if len(config["token"]) != 43 or not 60 <= config["seconds"] <= 18000:
            raise ValueError("Invalid sealed session configuration")
        self.recipient = recipient_id(config["recipient"])
        self.output.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.instance_lock = InstanceLock(self.root)
        self.vault, self.store = Vault(self.root), Store(self.root)
        self.store.bind(self.vault)
        self.vault.save("network", {"kind": "direct"})
        self.store.set_setting("route_policy", {"exposure": "tunnel", "outside_enabled": False})
        self.store.set_setting("parameters", {"dialog_limit": 20000, "export_max_gib": 4})
        self.collector = Collector(self.store, self.vault, client_factory)
        self.account_export = AccountExport(self.collector, self.store, self.vault)
        self.account_export.packaging_copies = 2
        self.account_job = None
        self.chats_task, self.chat_results, self.current_chat = None, None, None
        self.secret_mode = False
        self.provision_secret_module()
        self.selection = None
        receipt = run_receipt(self.store, self.vault)
        self.collector.run_id = receipt["run_id"]
        self.store.append("collector.started", receipt)
        self.store.append("sealed.started", {"format": "tgwitness-sealed-run-v1",
            "recipient_sha256": self.recipient, "context": config["context"],
            "deadline_seconds": config["seconds"], "session_import_allowed": False,
            "meaning": "Fresh Telegram login; selected chat or account data. Runtime trust depends on the external attestation."})
        self.lock = asyncio.Lock()
        self.phase, self.reason = "login", None
        self.revocation = None
        self.started, self.closed = time.monotonic(), False
        self.monitor_task = None
        self.finish_task = None
        self.assessment = None
        self.collection_started = None
        self.media_bytes_at, self.media_bytes = 0, 0

    def time_budget(self, account=None):
        remaining = max(0, int(self.config["seconds"] - (time.monotonic() - self.started)))
        account = account if account is not None else self.account_export.public(self.account_job) if self.account_job else {}
        if self.chat_results is not None and self.phase == "collecting":
            current = (self.collector.export_state or {}).get("captured", 0) if self.current_chat is not None else 0
            seen = sum(item.get("captured") or 0 for item in self.chat_results) + (current or 0)
            account = {"counts": {"messages_seen": seen, "unique_media_bytes": 0},
                       "acquisition": {"history_complete": False, "bytes_preserved": seen * 2048}}
        elif not self.account_job and self.phase == "collecting":
            history = self.collector.history.status()
            if time.monotonic() - self.media_bytes_at >= 5:
                with self.store.reading() as db:
                    self.media_bytes = db.execute(
                        "SELECT coalesce(sum(estimated_bytes),0) FROM media_jobs WHERE state='done'").fetchone()[0]
                self.media_bytes_at = time.monotonic()
            account = {"counts": {"messages_seen": history.get("captured", 0), "unique_media_bytes": self.media_bytes},
                       "acquisition": {"history_complete": history.get("phase") in {"complete", "incomplete"},
                                       "bytes_preserved": history.get("captured", 0) * 2048}}
        waiting = max(0, int((account.get("wait_until") or 0) - time.time()))
        elapsed = max(0, time.monotonic() - self.collection_started) if self.collection_started is not None else 0
        return export_budget.progress(self.assessment.get("time_plan") if self.assessment else None,
                                      account, remaining, self.config["seconds"], elapsed, waiting)

    def status(self):
        account = self.account_export.public(self.account_job) if self.account_job else None
        return {"phase": self.phase, "login": self.collector.phase, "reason": self.reason,
                "authorized": bool(self.store.get_setting("account", None)),
                "remaining_seconds": max(0, int(self.config["seconds"] - (time.monotonic() - self.started))),
                "history": self.collector.history.status(), "media": self.store.media_stats(),
                "capture": capture_settings(self.store),
                "selection": self.selection,
                "selection_sha256": selection_hash(self.selection) if self.selection else None,
                "account_export": account, "time_budget": self.time_budget(account),
                "chat_exports": self.chat_progress(),
                "secret": self.secret_status(),
                "recipient_sha256": self.recipient, "context": self.config["context"], "revocation": self.revocation}

    def chat_progress(self):
        if self.chat_results is None:
            return None
        current = self.collector.export_public() if self.current_chat is not None else None
        return {"total": len(self.selection["chat_ids"]), "kept": list(self.chat_results), "current_chat": self.current_chat,
                "current": {key: current.get(key) for key in ("phase", "captured", "total", "eta_seconds", "stage")}
                if current else None}

    def require_login(self):
        if self.phase != "login" or self.store.get_setting("account", None):
            raise ValueError("This capsule already has an account or has finished")

    def require_selection(self, chat_id):
        if self.phase != "login" or not self.store.get_setting("account", None):
            raise ValueError("Authorize a fresh Telegram session first")
        if chat_id is not None and chat_id not in self.collector.dialog_cache:
            raise ValueError("Select a chat from this account's dialog list")

    async def preview(self, selection):
        self.require_selection(selection.chat_id)
        if selection.mode == "account":
            from .export_preflight import preview
            result = await preview(self.account_export, selection.account_options.model_dump())
        elif selection.mode == "chats":
            result = None
            for chat_id in selection.chat_ids:
                self.require_selection(chat_id)
                part = await preview_capture(self.collector, chat_id, normalize_capture(selection.capture.model_dump()),
                                             self.status()["remaining_seconds"])
                if result is None:
                    result = part
                    continue
                result["sample"]["chats"] += part["sample"]["chats"]
                for key in ("messages_examined", "known_download_bytes", "known_hash_source_bytes",
                            "hash_manifest_estimate_bytes", "unknown_size_files", "excluded_attachments"):
                    result["sample"][key] = result["sample"].get(key, 0) + part["sample"].get(key, 0)
                result["sample"]["performed"] = result["sample"].get("performed") and part["sample"].get("performed")
                result["can_start"] = result["can_start"] and part["can_start"]
                result["issues"] += part["issues"]
            result["sample"]["visible_selected_chats"] = len(selection.chat_ids)
        else:
            result = await preview_capture(self.collector, selection.chat_id,
                                       normalize_capture(selection.capture.model_dump()),
                                       self.status()["remaining_seconds"])
        result["remaining_seconds"] = self.status()["remaining_seconds"]
        result["can_start"] = result["can_start"] and result["remaining_seconds"] > 0
        result["selection"] = selection.settings()
        result["selection_sha256"] = selection_hash(result["selection"])
        options = selection.account_options.model_dump() if selection.mode == "account" else selection.capture.model_dump()
        result["time_plan"] = export_budget.plan(result["sample"], options, result["remaining_seconds"], self.config["seconds"])
        if not result["time_plan"]["unknown"]:
            result["estimated_seconds"] = result["time_plan"]["estimated_total_seconds"]
            result["total_output_bytes"] = result["time_plan"]["output_bytes"]
        result["can_start"] = result["can_start"] and result["time_plan"]["fit"] != "no_collection_time"
        self.assessment = result
        return result

    async def begin_selection(self, selection):
        if self.assessment and self.assessment["selection_sha256"] != selection_hash(selection.settings()):
            self.assessment = None
        if self.assessment is None:
            await self.preview(selection)
        options = selection.account_options.model_dump() if selection.mode == "account" else selection.capture.model_dump()
        self.assessment["time_plan"] = export_budget.plan(self.assessment["sample"], options,
            self.status()["remaining_seconds"], self.config["seconds"])
        if not self.assessment["can_start"]:
            raise ValueError("Not enough disk or time remains for the selected capture and packaging.")
        if self.assessment["time_plan"]["fit"] == "no_collection_time":
            raise ValueError("Not enough time remains for collection and archive packaging.")
        if selection.mode == "chat":
            return await self.begin(selection.chat_id, selection.capture)
        if selection.mode == "chats":
            return await self.begin_chats(selection)
        if selection.mode == "secret":
            return await self.begin_secret(selection)
        self.require_selection(None)
        if self.status()["remaining_seconds"] <= 0:
            raise ValueError("No capture time remains.")
        options = selection.account_options.model_dump()
        job = await self.account_export.start(options, archive_name=ACCOUNT_MEMBER)
        self.account_job = job["id"]
        self.selection = selection.settings()
        self.store.append("sealed.selection", {"mode": "account", "options": options,
            "selection": self.selection, "selection_sha256": selection_hash(self.selection),
            "free_disk_bytes": shutil.disk_usage(self.root).free, "remaining_seconds": self.status()["remaining_seconds"],
            "transport": options["transport"], "total_size_and_duration": "estimated",
            "time_plan": self.assessment["time_plan"] if self.assessment else None})
        self.phase = "collecting"
        self.collection_started = time.monotonic()

    async def begin_chats(self, selection):
        for chat_id in selection.chat_ids:
            self.require_selection(chat_id)
        settings = normalize_capture(selection.capture.model_dump())
        free = shutil.disk_usage(self.root).free
        if free < self.collector.param("media_min_free_mb") * 1024**2 or self.status()["remaining_seconds"] <= 0:
            raise ValueError("Not enough free disk or capture time")
        self.store.set_setting("capture", settings)
        self.selection = selection.settings()
        self.store.append("sealed.selection", {"mode": "chats", "chat_ids": list(selection.chat_ids), "capture": settings,
            "selection": self.selection, "selection_sha256": selection_hash(self.selection),
            "free_disk_bytes": free, "remaining_seconds": self.status()["remaining_seconds"],
            "transport": "regular", "total_size_and_duration": "estimated",
            "time_plan": self.assessment["time_plan"] if self.assessment else None})
        self.chat_results = []
        self.phase = "collecting"
        self.collection_started = time.monotonic()
        self.chats_task = asyncio.create_task(self.run_chats(list(selection.chat_ids)))

    async def run_chats(self, chat_ids):
        """Export each selected chat in turn with the workspace chat export: profile, authors, admin log, ID gaps."""
        for chat_id in chat_ids:
            self.current_chat = chat_id
            try:
                await self.collector.start_export(chat_id, {"language": "en"})
                await asyncio.gather(self.collector.export_task, return_exceptions=True)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                payload = {"chat_id": chat_id, "title": (self.collector.dialog_cache.get(chat_id) or {}).get("title"),
                           "file": None, "complete": False, "phase": "failed", "captured": 0, "error": type(exc).__name__}
                self.store.append("sealed.chat_export", payload)
                self.chat_results.append({k: payload.get(k) for k in ("chat_id", "title", "file", "complete", "phase",
                                                                      "captured", "message_ids")})
                continue
            self.keep_chat_export(chat_id)
        self.current_chat = None

    def keep_chat_export(self, chat_id, snapshot=None):
        state = self.collector.export_state or {}
        source = snapshot or (self.collector.export_path if state.get("ready") else None)
        complete = snapshot is None and state.get("phase") == "done"
        payload = {"chat_id": chat_id, "title": (self.collector.dialog_cache.get(chat_id) or {}).get("title"),
                   "file": None, "complete": complete, "phase": "snapshot" if snapshot else state.get("phase"),
                   "captured": state.get("captured"), "error": state.get("error")}
        if source is not None:
            folder = self.root / "chat-exports"
            folder.mkdir(mode=0o700, exist_ok=True)
            name = f"chat-export-{sum(1 for item in self.chat_results if item.get('file')) + 1:03d}.zip"
            shutil.move(str(source), folder / name)
            if self.collector.export_path == source:
                self.collector.export_path = None
            payload.update(file=name, sha256=file_sha(folder / name), bytes=(folder / name).stat().st_size)
            if snapshot is None:
                payload["message_ids"] = message_id_summary(folder / name)
        self.store.append("sealed.chat_export", payload)
        self.chat_results.append({k: payload.get(k) for k in ("chat_id", "title", "file", "complete", "phase", "captured",
                                                              "message_ids")})

    async def stop_chats(self, cancel):
        """Keep a signed partial snapshot of the chat in progress, then stop the remaining chat exports."""
        if self.chats_task is None or self.chats_task.done():
            return
        chat_id, state, snapshot = self.current_chat, self.collector.export_state or {}, None
        if not cancel and chat_id is not None and state.get("phase") == "running":
            try:
                snapshot = await complete_in_thread(self.collector.live_snapshot, state["id"])
            except Exception:
                snapshot = None
        self.chats_task.cancel()
        await asyncio.gather(self.chats_task, return_exceptions=True)
        if chat_id is not None and not cancel:
            self.keep_chat_export(chat_id, Path(snapshot) if snapshot else None)
        self.current_chat = None

    def provision_secret_module(self):
        from . import secret_module
        source = IMAGE_MODULES / secret_module.FILE
        if not source.is_file() or source.is_symlink():
            secret_module.home = self.root / "modules"
            return
        target = self.root / "modules"
        target.mkdir(mode=0o700, exist_ok=True)
        shutil.copyfile(source, target / secret_module.FILE)
        secret_module.restore(self.root)

    def secret_status(self):
        if not self.secret_mode:
            return None
        from . import secret_chats
        view = secret_chats.of(self.collector).view()
        return {key: view.get(key) for key in ("connected", "error", "chats", "people", "records", "interaction_problem",
                                                "pending_files")}

    async def begin_secret(self, selection):
        from . import secret_chats, secret_module
        self.require_selection(None)
        if not secret_chats.available():
            raise ValueError("This runner has no checked pseudo-secret module, so secret chats cannot be captured here.")
        settings = normalize_capture(selection.capture.model_dump())
        self.store.set_setting("capture", settings)
        self.store.set_setting(secret_chats.SETTING, {"enabled": True, "accept_incoming": selection.accept_incoming})
        self.selection = selection.settings()
        module = secret_module.describe()
        self.store.append("secret_chat.module_installed", {
            **{key: module.get(key) for key in ("name", "version", "commit", "sha256", "source", "license", "state")},
            "route": "runner_image", "meaning": "The pseudo-secret protocol module was built into this runner's image "
            "from the pinned upstream archive and matched the SHA-256 fixed in this release before it was loaded."})
        self.store.append("sealed.selection", {"mode": "secret", "secret_peer": selection.secret_peer,
            "accept_incoming": selection.accept_incoming, "capture": settings, "selection": self.selection,
            "selection_sha256": selection_hash(self.selection), "free_disk_bytes": shutil.disk_usage(self.root).free,
            "remaining_seconds": self.status()["remaining_seconds"], "transport": "regular",
            "total_size_and_duration": "observed during the run"})
        self.secret_mode = True
        await self.collector.restore()
        chats = secret_chats.of(self.collector)
        if chats.manager is None:
            await chats.attach(self.collector.client)
        self.phase = "collecting"
        self.collection_started = time.monotonic()
        if selection.secret_peer is not None:
            user = int(selection.secret_peer) if selection.secret_peer.isdigit() else selection.secret_peer
            await chats.create(user)

    def require_secret(self):
        if not self.secret_mode or self.phase != "collecting":
            raise ValueError("No secret chat capture is running.")
        from . import secret_chats
        return secret_chats.of(self.collector)

    async def resume(self):
        if self.phase != "collecting":
            raise ValueError("No capture to resume.")
        if self.chats_task:
            raise ValueError("Chat exports continue on their own; there is nothing to resume.")
        if self.account_job:
            return await self.account_export.resume(self.account_job)
        return await self.collector.history.resume()

    async def begin(self, chat_id, capture=None):
        self.require_selection(chat_id)
        settings = normalize_capture((capture or Selection(chat_id=chat_id).capture).model_dump())
        free = shutil.disk_usage(self.root).free
        if free < self.collector.param("media_min_free_mb") * 1024**2 or self.status()["remaining_seconds"] <= 0:
            raise ValueError("Not enough free disk or capture time")
        self.store.set_setting("capture", settings)
        self.selection = Selection(chat_id=chat_id, capture=settings).settings()
        self.store.append("sealed.selection", {"chat_id": chat_id, "capture": settings,
            "selection": self.selection, "selection_sha256": selection_hash(self.selection),
            "free_disk_bytes": free, "remaining_seconds": self.status()["remaining_seconds"],
            "transport": "regular", "total_size_and_duration": "estimated",
            "time_plan": self.assessment["time_plan"] if self.assessment else None})
        chat = self.collector.dialog_cache[chat_id]
        self.store.set_target(chat_id, chat["title"], chat["kind"], True)
        await self.collector.history.start()
        self.phase = "collecting"
        self.collection_started = time.monotonic()

    async def revoke(self):
        results = []
        clients = [c for c in (self.collector.client, self.collector.login_client) if c is not None]
        for client in clients:
            try:
                async def logout():
                    if not client.is_connected():
                        await client.connect()
                    return bool(await client.log_out())
                results.append("revoked" if await asyncio.wait_for(logout(), 15) else "not_confirmed")
            except Exception:
                results.append("not_confirmed")
        self.vault.save("credentials", {})
        return "not_confirmed" if "not_confirmed" in results else "revoked" if results else "no_session"

    def write_parts(self, source=None):
        with EncryptedParts(self.output, self.vault, self.config) as outgoing:
            if source is not None:
                with source.open("rb") as incoming:
                    for block in iter(lambda: incoming.read(1024**2), b""):
                        outgoing.write(block)
            else:
                export_file(self.store, self.vault, "zip", compact=True, output_stream=outgoing,
                            max_uncompressed_bytes=1024 * 1024**3)

    async def finish(self, reason, cancel=False):
        if self.phase in TERMINAL:
            return
        had_capture = self.phase == "collecting"
        self.phase, self.reason = "sealing", reason
        try:
            acquisition_error = None
            if self.account_job:
                try:
                    await self.account_export.pause(self.account_job)
                    if not cancel:
                        job = await self.account_export.finalize_partial(self.account_job, "Capture ended: " + reason)
                        path = self.account_export.result_path(self.account_job)
                        self.store.append("sealed.account_export", {"job_id": self.account_job, "file": ACCOUNT_MEMBER,
                            "sha256": file_sha(path), "bytes": path.stat().st_size, "complete_within_scope": job["phase"] == "done",
                            "coverage": job["coverage"], "counts": job["counts"]})
                except Exception as exc:
                    acquisition_error = exc
            if self.chats_task:
                try:
                    await self.stop_chats(cancel)
                except Exception as exc:
                    acquisition_error = acquisition_error or exc
            pending = self.collector.login_client
            before_stop = await self.revoke() if pending is not None else "no_session"
            stop_error = None
            try:
                await self.collector.stop(shutdown=True)
            except Exception as exc:
                stop_error = exc
            after_stop = await self.revoke()
            outcomes = (before_stop, after_stop)
            revoked = ("not_confirmed" if "not_confirmed" in outcomes else
                       "revoked" if "revoked" in outcomes else "no_session")
            self.revocation = revoked
            self.store.append("sealed.finished", {"reason": reason, "revocation": revoked,
                "history": self.collector.history.status(), "media": self.store.media_stats(),
                "account_export": self.account_export.public(self.account_job) if self.account_job else None,
                "chat_exports": self.chat_results,
                "meaning": "Partial reads, skipped attachments and failed downloads remain visible in this journal."})
            if acquisition_error:
                raise acquisition_error
            if stop_error:
                raise stop_error
            if cancel or not had_capture:
                self.phase = "cancelled"
                private_write(self.output / "result.json", canonical({"phase": self.phase}))
                return
            try:
                nested = bool(self.account_job) or self.chat_results is not None
                archive = await complete_in_thread(partial(export_file, self.store, self.vault, "zip", compact=nested))
            except (BundleSizeLimit, OSError) as exc:
                disk_full = isinstance(exc, OSError) and (exc.errno in (errno.ENOSPC, errno.EDQUOT)
                                                         or getattr(exc, "winerror", None) == 112)
                if not isinstance(exc, BundleSizeLimit) and not disk_full:
                    raise
                self.store.append("sealed.packaging", {"mode": "compact",
                    "reason": "disk_full" if disk_full else "archive_size_limit",
                    "full_journal": True, "preserved_media_omitted": False})
                try:
                    archive = await complete_in_thread(partial(export_file, self.store, self.vault, "zip", compact=True))
                except (BundleSizeLimit, OSError) as compact_error:
                    if isinstance(compact_error, OSError) and not (compact_error.errno in (errno.ENOSPC, errno.EDQUOT)
                            or getattr(compact_error, "winerror", None) == 112):
                        raise
                    await complete_in_thread(self.write_parts)
                    archive = None

            if archive is not None and archive.stat().st_size > PART_BYTES:
                await complete_in_thread(self.write_parts, archive)
                archive.unlink()
                archive = None
            if archive is not None:
                shutil.move(str(archive), self.output / "evidence.zip")
            self.phase = "sealed"
            private_write(self.output / "result.json", canonical({"phase": "sealed"} if archive is not None else SEALED_RESULT))
        except Exception as exc:
            failure = type(exc).__name__
            (self.output / "evidence.zip").unlink(missing_ok=True)
            if had_capture and not cancel and await self.salvage(failure):
                self.phase, self.reason = "sealed", "salvaged_after_" + failure
                return
            self.phase, self.reason = "failed", failure
            private_write(self.output / "result.json", canonical({"phase": "failed"}))

    async def salvage(self, failure):
        """Keep what was collected when acquisition or full packaging fails: the signed journal records the failure."""
        try:
            self.store.append("sealed.failure", {"error": failure, "salvaged": "compact_journal",
                "meaning": "Collection or full packaging failed. This archive is the compact signed journal of everything "
                           "recorded before the failure; it is incomplete within the selected scope."})
            for leftover in self.output.glob("delivery-*"):
                leftover.unlink(missing_ok=True)
            archive = await complete_in_thread(partial(export_file, self.store, self.vault, "zip", compact=True))
            if archive.stat().st_size > PART_BYTES:
                await complete_in_thread(self.write_parts, archive)
                archive.unlink()
                private_write(self.output / "result.json", canonical(SEALED_RESULT))
            else:
                shutil.move(str(archive), self.output / "evidence.zip")
                private_write(self.output / "result.json", canonical({"phase": "sealed"}))
            return True
        except Exception:
            (self.output / "evidence.zip").unlink(missing_ok=True)
            return False

    async def monitor(self):
        while self.phase not in TERMINAL:
            await asyncio.sleep(.2)
            async with self.lock:
                if self.phase in TERMINAL:
                    return
                if time.monotonic() - self.started >= self.config["seconds"]:
                    await self.finish("deadline")
                elif self.phase == "collecting":
                    if self.time_budget()["collection_seconds"] <= 0:
                        await self.finish("packaging_reserve")
                        continue
                    if self.account_job:
                        if self.account_export.public(self.account_job).get("ready"):
                            await self.finish("account_export_finished")
                        elif self.account_export.storage_pressure():
                            await self.finish("storage_limit")
                        continue
                    if self.secret_mode:
                        continue
                    if self.chats_task:
                        if self.chats_task.done():
                            await self.finish("chat_exports_finished")
                        continue
                    state = self.collector.history.status()
                    pending = sum(n for k, n in self.store.media_stats().items() if k in ("queued", "retry", "running"))
                    if state["phase"] in ("complete", "incomplete") and not pending:
                        await self.finish("history_and_media_finished")

    async def close(self):
        if self.closed:
            return
        if self.finish_task:
            await asyncio.shield(self.finish_task)
        if self.monitor_task and self.phase == "sealing":

            await asyncio.shield(self.monitor_task)
        if self.monitor_task:
            self.monitor_task.cancel()
            await asyncio.gather(self.monitor_task, return_exceptions=True)
        async with self.lock:
            if self.phase not in TERMINAL:
                await self.finish("server_shutdown", cancel=True)
            await self.collector.stop(shutdown=True)
            await self.account_export.close()
            self.store.close()
            self.instance_lock.close()
            self.closed = True


def message_id_summary(path):
    """First and last ID, present and missing counts of a finished chat export; None when it cannot be read."""
    import zipfile
    try:
        with zipfile.ZipFile(path) as archive:
            info = json.loads(archive.read("message-ids.json"))
    except (OSError, KeyError, ValueError, zipfile.BadZipFile):
        return None
    ranges = info.get("missing_ranges") or []
    return {"numbered_per_chat": info.get("numbered_per_chat") is True, "first_id": info.get("first_id"),
            "last_id": info.get("last_id"), "present": info.get("present"), "missing": info.get("missing"),
            "missing_runs": len(ranges), "largest_runs": sorted(ranges, key=lambda r: r[0] - r[1])[:5]}


def create_app(root, output, config, client_factory=WitnessClient):
    @asynccontextmanager
    async def lifespan(app):
        session = Session(root, output, config, client_factory)
        app.state.session = session
        session.monitor_task = asyncio.create_task(session.monitor())
        try:
            yield
        finally:
            await session.close()

    app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
    app.add_middleware(RequestLimit, max_body=8192, path_limits=False)
    token_digest = hashlib.sha256(config["token"].encode()).digest()

    @app.middleware("http")
    async def restricted(request, call_next):
        path = request.url.path
        if path.startswith("/api/"):
            supplied = request.headers.get("authorization", "")
            good = supplied.startswith("Bearer ") and secrets.compare_digest(
                hashlib.sha256(supplied[7:].encode()).digest(), token_digest)
            if not good:
                return JSONResponse({"detail": "Access denied"}, status_code=401,
                                    headers={"Cache-Control": "no-store"})
            origin = request.headers.get("origin")
            if origin and urlsplit(origin).netloc.lower() != request.headers.get("host", "").lower():
                return JSONResponse({"detail": "Origin denied"}, status_code=403)
        response = await call_next(request)
        response.headers.update({"Cache-Control": "no-store", "Referrer-Policy": "no-referrer",
            "X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY",
            "Content-Security-Policy": "default-src 'none'; script-src 'self'; style-src 'self'; "
                "connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'none'"})
        return response

    @app.exception_handler(RequestValidationError)
    async def invalid(request, exc):
        return JSONResponse({"detail": "Invalid request fields"}, status_code=422)

    async def operation(call, *args, login=False, fresh=False):
        session = app.state.session
        async with session.lock:
            if session.phase in TERMINAL or session.phase == "sealing":
                raise HTTPException(409, "This capsule has finished")
            try:
                if login:
                    session.require_login()
                if fresh and (session.collector.login_client is not None or session.collector.qr_task is not None):
                    # A new phone or QR sign-in replaces an unfinished one: the code may have expired or never arrived.
                    await session.collector.cancel_login()
                return await asyncio.wait_for(call(*args), 120)
            except Exception as exc:
                raise HTTPException(400, describe(exc)) from None

    @app.get("/")
    async def index():
        return FileResponse(STATIC / "sealed.html")

    @app.get("/sealed.js")
    async def script():
        return FileResponse(STATIC / "sealed.js", media_type="text/javascript")

    @app.get("/sealed-locales.js")
    async def locales():
        return FileResponse(STATIC / "sealed-locales.js", media_type="text/javascript")

    @app.get("/sealed.css")
    async def styles():
        return FileResponse(STATIC / "sealed.css", media_type="text/css")

    @app.get("/style.css")
    async def workspace_styles():
        return FileResponse(STATIC / "style.css", media_type="text/css")

    @app.get("/theme.js")
    async def workspace_theme():
        return FileResponse(STATIC / "theme.js", media_type="text/javascript")

    @app.get("/mark.svg")
    async def workspace_mark():
        return FileResponse(STATIC / "mark.svg", media_type="image/svg+xml")

    @app.get("/api/status")
    async def status():
        return app.state.session.status()

    @app.post("/api/phone")
    async def phone(body: Phone, request: Request):
        from .client_identity import language_defaults
        languages = language_defaults(request.headers.get("x-tgwitness-language"),
                                      request.headers.get("x-tgwitness-system-language") or request.headers.get("accept-language"))
        return await operation(app.state.session.collector.start_phone, body.phone,
                               body.api_id, body.api_hash, None, languages, login=True, fresh=True)

    @app.post("/api/code")
    async def code(body: Code):
        return await operation(app.state.session.collector.confirm_code, body.code, login=True)

    @app.post("/api/password")
    async def password(body: Password):
        return await operation(app.state.session.collector.confirm_password, body.password, login=True)

    @app.post("/api/qr")
    async def qr(body: Login, request: Request):
        import qrcode
        from qrcode.image.svg import SvgPathImage
        from .client_identity import language_defaults
        languages = language_defaults(request.headers.get("x-tgwitness-language"),
                                      request.headers.get("x-tgwitness-system-language") or request.headers.get("accept-language"))
        result = await operation(app.state.session.collector.start_qr, body.api_id, body.api_hash,
                                 None, languages, login=True, fresh=True)
        output = io.BytesIO()
        qrcode.make(result.pop("url"), image_factory=SvgPathImage).save(output)
        return {**result, "svg": output.getvalue().decode()}

    @app.get("/api/qr/{login_id}")
    async def qr_status(login_id: str):
        return app.state.session.collector.poll_qr(login_id)

    @app.get("/api/dialogs")
    async def dialogs():
        if app.state.session.phase != "login":
            raise HTTPException(409, "Chat selection is already fixed")
        return await operation(app.state.session.collector.dialogs)

    @app.post("/api/collect")
    async def collect(body: Selection):
        await operation(app.state.session.begin_selection, body)
        return app.state.session.status()

    @app.post("/api/preflight")
    async def preflight(body: Selection):
        return await operation(app.state.session.preview, body)

    @app.post("/api/resume")
    async def resume():
        return await operation(app.state.session.resume)

    @app.post("/api/finish")
    async def finish():
        session = app.state.session
        async with session.lock:
            if session.phase != "collecting" or session.finish_task:
                raise HTTPException(409, "No active collection to finish")
            async def finalize():
                async with session.lock:
                    await session.finish("user_finish")
            session.finish_task = asyncio.create_task(finalize())
        return JSONResponse({"phase": "sealing"}, status_code=202)

    class SecretUser(StrictBody):
        user: str = Field(min_length=1, max_length=64, pattern=r"^(@?[A-Za-z][A-Za-z0-9_]{3,31}|[0-9]{1,20})$")

    class SecretText(StrictBody):
        text: str = Field(min_length=1, max_length=4096)

    async def secret_call(name, *args):
        session = app.state.session
        async with session.lock:
            try:
                chats = session.require_secret()
                result = await asyncio.wait_for(getattr(chats, name)(*args), 120)
            except Exception as exc:
                raise HTTPException(400, describe(exc)) from None
            return {"result": result if name != "send" else str(result), "secret": session.secret_status()}

    @app.post("/api/secret/create")
    async def secret_create(body: SecretUser):
        user = body.user.removeprefix("@")
        return await secret_call("create", int(user) if user.isdigit() else user)

    @app.post("/api/secret/{chat_id}/accept")
    async def secret_accept(chat_id: int):
        return await secret_call("accept", chat_id)

    @app.post("/api/secret/{chat_id}/send")
    async def secret_send(chat_id: int, body: SecretText):
        return await secret_call("send", chat_id, body.text)

    @app.post("/api/secret/{chat_id}/close")
    async def secret_close(chat_id: int):
        return await secret_call("close", chat_id)

    @app.post("/api/cancel")
    async def cancel():
        session = app.state.session
        async with session.lock:
            await session.finish("user_cancel", cancel=True)
        return {"phase": session.phase}

    return app


def main():
    import uvicorn
    parser = argparse.ArgumentParser(description="Disposable restricted Telegram capture server")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_bytes())

    logging.disable(logging.CRITICAL)
    uvicorn.run(create_app(args.data, args.out, config), host="0.0.0.0", port=8787,
                access_log=False, log_level="critical", proxy_headers=False, timeout_keep_alive=KEEP_ALIVE_SECONDS)


if __name__ == "__main__":
    main()
