import asyncio
import hashlib
import json
import logging
import secrets
import shutil
import time
from datetime import datetime, timezone

from telethon import utils
from telethon.errors import FloodWaitError
from telethon.tl import functions, types
from telethon.tl.tlobject import TLObject

from . import secret_module
from .monitoring import capture_settings
from .store import canonical, utcnow
from .workers import complete_in_thread

library = library_tl = VaultStorage = None
LOG = logging.getLogger("tgwitness.secret_chats")
SETTING = "secret_chats"
STATE = "secret_chats"
PENDING = "secret_chat_files"
HELD = "secret_chat_unwritten"
REFRESH_SECONDS = 30
LIVENESS_SECONDS = 120
LIVENESS_CHATS = 20
ENDED_BY_TELEGRAM = "Telegram reports the chat no longer exists"
HIDDEN = {"key", "iv"}
QUIET = {"DecryptedMessageActionRequestKey", "DecryptedMessageActionAcceptKey", "DecryptedMessageActionCommitKey",
         "DecryptedMessageActionAbortKey", "DecryptedMessageActionNoop", "DecryptedMessageActionNotifyLayer",
         "DecryptedMessageActionResend"}
UNAVAILABLE = "Pseudo-secret needs its protocol module, which is not installed yet."
SAME = ("direction", "seq_no", "text", "ttl", "reply_to_random_id", "entities", "media")
READ_MEANING = ("Sent from the panel: the other side sees its messages dated up to this time as read, and its app "
                "starts their self-destruct timers. TgWitness keeps its own copies.")
CONTENT_MEANING = ("Sent from the panel as an encrypted read notice for these messages: the other side sees them as "
                   "opened, and its app starts their self-destruct timers. TgWitness keeps its own copies.")
PEER_READ_MEANING = ("Telegram reported that the other side read this account's messages in this chat dated up to "
                     "max_date. Official apps start the self-destruct timers of those messages at this point.")
PEER_OPENED_MEANING = ("The other side reported these messages as opened. Official apps send this for viewed timed "
                       "messages and played voice or video messages. TgWitness keeps every earlier message.")


def unix(value):
    return int(value.timestamp()) if isinstance(value, datetime) else value


def moment(value):
    return datetime.fromtimestamp(value, timezone.utc).isoformat() if type(value) is int else None


def available():
    return library is not None


def bind():
    global library, library_tl, VaultStorage
    try:
        import telethon_secret_chat as module
        from telethon_secret_chat.schema import secret_tl
    except ImportError:
        return False

    class Storage(module.MemoryStorage):

        def __init__(self, vault):
            super().__init__()
            self.vault = vault
            saved = vault.read(STATE)
            if saved:
                state = decode(saved)
                if not all(isinstance(state.get(group), dict) for group in ("chats", "out", "in")):
                    raise ValueError("The saved secret-chat state is damaged.")
                self._state = state

        def _write(self):
            self.vault.save(STATE, encode(self._state))

    library, library_tl, VaultStorage = module, secret_tl, Storage
    return True


def of(collector):
    existing = getattr(collector, "secret_chats", None)
    if existing is None:
        existing = SecretChats(collector)
        collector.secret_chats = existing
    return existing


def settings(store):
    saved = store.get_setting(SETTING, {}) or {}
    return {"enabled": bool(saved.get("enabled")), "accept_incoming": bool(saved.get("accept_incoming"))}


def plain(value):
    if isinstance(value, TLObject) or library is not None and isinstance(value, library_tl.SecretTLObject):
        value = value.to_dict()
    if isinstance(value, dict):
        return {k: plain(v) for k, v in value.items() if k not in HIDDEN}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if isinstance(value, (bytes, bytearray)):
        return {"sha256": hashlib.sha256(value).hexdigest(), "bytes": len(value)}
    return value


def encode(value):
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [encode(v) for v in value]
    if isinstance(value, (bytes, bytearray)):
        return {"__bytes__": bytes(value).hex()}
    return value


def decode(value):
    if isinstance(value, dict):
        if set(value) == {"__bytes__"}:
            return bytes.fromhex(value["__bytes__"])
        return {k: decode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [decode(v) for v in value]
    return value


def running():
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True


def fingerprint(payload):
    return hashlib.sha256(canonical({key: (payload or {}).get(key) for key in SAME})).hexdigest()


def same(payload, earlier):
    return all(canonical(payload[key]) == canonical(earlier.get(key)) for key in SAME if key in payload)


def slot(entries, name, mark, field=None):
    existing = entries.get(name)
    if existing is not None and field:
        existing = existing.get(field)
    return name if existing is None or fingerprint(existing) == mark else name + ":" + mark


def display(value, field=None):
    if isinstance(value, dict):
        return {key: display(item, key) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [display(item, field) for item in value]
    if type(value) is int and (field in {"random_id", "random_ids", "reply_to_random_id"}
                               or abs(value) > 2**53 - 1):
        return str(value)
    return value


def retain_file(temporary, media_root):
    with temporary.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    size = temporary.stat().st_size
    target = media_root / digest
    repaired = None
    if target.is_symlink() or (target.exists() and not target.is_file()):
        raise ValueError("The attachment destination is not a regular file.")
    if target.exists():
        with target.open("rb") as stream:
            previous = hashlib.file_digest(stream, "sha256").hexdigest()
        if previous == digest and target.stat().st_size == size:
            temporary.unlink()
            return digest, size, repaired
        quarantine = media_root / (".corrupt-" + digest + "-" + secrets.token_hex(8))
        target.replace(quarantine)
        repaired = {"previous_sha256": previous, "retained_as": quarantine.name}
    temporary.replace(target)
    return digest, size, repaired


bind()


class SecretChats:
    def __init__(self, collector):
        self.collector = collector
        self.manager = self.client = None
        self.lock = asyncio.Lock()
        self.seen = set()
        self.tasks = set()
        self.downloads = {}
        self.file_worker = None
        self.file_wakeup = asyncio.Event()
        self.error = None
        self.asked = set()
        self.early = {}
        self.open_at = {}

    @property
    def store(self):
        return self.collector.store

    def note(self, kind, payload):
        return self.store.append("secret_chat." + kind, payload)

    def hold(self, name, payload):
        held = self.collector.vault.read(HELD) or {}
        held[slot(held, name, fingerprint(payload))] = payload
        self.collector.vault.save(HELD, held)

    def release(self, name):
        held = self.collector.vault.read(HELD) or {}
        if held.pop(name, None) is not None:
            self.collector.vault.save(HELD, held)

    def write_held(self):
        kept = 0
        for name, payload in list((self.collector.vault.read(HELD) or {}).items()):
            try:
                self.write_message(payload)
            except Exception:
                LOG.exception("A held secret-chat message could not be written")
                kept += 1
                continue
            self.release(name)
        return kept

    def peer(self, chat_id):
        try:
            return self.manager.status(chat_id).peer_user_id
        except Exception:
            return None

    def listen(self, client):
        if client in self.early or not available() or not settings(self.store)["enabled"]:
            return
        held = []

        async def keep(update):
            if self.client is not client and len(held) < 2000 and isinstance(
                    update, (types.UpdateEncryption, types.UpdateNewEncryptedMessage)):
                held.append(update)

        client.add_event_handler(keep)
        self.early[client] = keep, held

    async def attach(self, client):
        if not available() or not settings(self.store)["enabled"]:
            return False
        async with self.lock:
            if self.manager and self.client is client:
                self.resume_files()
                return True
            await self._detach()
            manager = library.SecretChatManager(client, storage=VaultStorage(self.collector.vault))
            for name in ("ChatRequested", "ChatReady", "ChatClosedEvent", "MessageReceived", "ServiceActionReceived",
                         "DecryptFailed", "SendFailed"):
                manager.on(name, getattr(self, "on_" + name))
            self.manager, self.client = manager, client
            keep, held = self.early.pop(client, (None, ()))
            if keep:
                client.remove_event_handler(keep)
            try:
                await manager.start()
            except BaseException:
                self.manager = self.client = None
                raise
            for update in held:
                try:
                    await manager._subscription(update)
                except Exception:
                    LOG.exception("An update received before secret chats started could not be applied")
            self.write_held()
            self.resume_files()
            self.spawn(self.refresh(manager, client))
            return True

    async def refresh(self, manager, client):
        checked = time.monotonic()
        while self.manager is manager:
            await asyncio.sleep(REFRESH_SECONDS)
            if self.manager is manager and client.is_connected() and any(
                    getattr(chat.state, "name", "") != "CLOSED" for chat in manager.list()):
                try:
                    await client.catch_up()
                except Exception:
                    LOG.exception("Secret chat updates could not be refreshed")
                if time.monotonic() - checked >= LIVENESS_SECONDS:
                    checked = time.monotonic()
                    await self.check_open(manager)

    async def check_open(self, manager):
        accepted = [chat for chat in manager.list() if getattr(chat.state, "name", "") == "READY" and not chat.is_outbound]
        for chat in accepted[:LIVENESS_CHATS]:
            if self.manager is not manager:
                return
            try:
                await manager._send_action(manager._entity(chat.id), library_tl.DecryptedMessageActionNoop())
            except library.ChatClosed:
                continue
            except Exception as exc:
                LOG.warning("Secret chat %s could not be checked: %s", chat.id, type(exc).__name__)
                continue
            self.open_at[chat.id] = utcnow()

    async def detach(self):
        async with self.lock:
            await self._detach()

    async def _detach(self):
        manager, self.manager, self.client = self.manager, None, None
        for task in list(self.tasks):
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.file_worker = None
        self.downloads.clear()
        if manager is not None:
            try:
                await asyncio.wait_for(manager.stop(), 15)
            except Exception:
                LOG.exception("Secret chats did not stop cleanly")

    def require(self):
        if not available():
            raise ValueError(UNAVAILABLE)
        if not settings(self.store)["enabled"]:
            raise ValueError("Turn on pseudo-secret for this account first.")
        if self.manager is None or self.client is None or not self.client.is_connected():
            raise ValueError("Connect this account to Telegram first.")
        return self.manager

    def recorded(self, kind, chat_id, random_id=None):
        query = "SELECT 1 FROM events WHERE kind=? AND json_extract(payload,'$.secret_chat_id')=?"
        values = ["secret_chat." + kind, chat_id]
        if random_id is not None:
            query += " AND json_extract(payload,'$.random_id')=?"
            values.append(random_id)
        with self.store.lock:
            return self.store.db.execute(query + " LIMIT 1", values).fetchone() is not None

    def earlier(self, kind, chat_id, random_id):
        with self.store.lock:
            return [(row[0], json.loads(row[1])) for row in self.store.db.execute(
                "SELECT seq, payload FROM events WHERE kind=? AND json_extract(payload,'$.secret_chat_id')=?"
                " AND json_extract(payload,'$.random_id')=? ORDER BY seq", ("secret_chat." + kind, chat_id, random_id))]

    def matching(self, payload):
        earlier = self.earlier("message", payload.get("secret_chat_id"), payload.get("random_id"))
        return next((seq for seq, saved in earlier if same(payload, saved)), None), earlier

    def write_message(self, payload):
        found, earlier = self.matching(payload)
        if found is None:
            if earlier:
                payload = {**payload, "same_random_id_as": [seq for seq, _ in earlier]}
            found = self.note("message", payload)["seq"]
        return found

    def has_file(self, chat_id, random_id, message):
        return any(saved.get("message_event") in (None, message) for _, saved in self.earlier("file", chat_id, random_id))

    def on_ChatRequested(self, event):
        accept = settings(self.store)["accept_incoming"]
        if not self.recorded("requested", event.chat_id):
            self.note("requested", {"secret_chat_id": event.chat_id, "peer_user_id": event.peer_user_id,
                                    "direction": "in", "accepted_automatically": accept})
        if accept:
            self.spawn(self.accept(event.chat_id, automatic=True))

    def on_ChatReady(self, event):
        payload = {"secret_chat_id": event.chat_id, "peer_user_id": event.peer_user_id,
                   "key_fingerprint": event.key_fingerprint}
        if event.key_hash:
            payload["key_visualization"] = library.key_visualization(event.key_hash).hex
        self.note("ready", payload)

    def on_ChatClosedEvent(self, event):
        payload = {"secret_chat_id": event.chat_id, "reason": event.reason,
                   "history_deleted_by_peer": bool(event.history_deleted),
                   "journal_copy": "kept; the journal is append-only"}
        if event.reason == ENDED_BY_TELEGRAM:
            payload["open_at_least_until"] = self.open_at.get(event.chat_id)
            payload["meaning"] = ("Telegram does not tell the side that accepted a secret chat when the other side ends "
                                  "it. TgWitness found the chat ended at this point; it ended after open_at_least_until, "
                                  "or after the chat was accepted when that is empty.")
        self.open_at.pop(event.chat_id, None)
        self.note("closed", payload)

    def on_MessageReceived(self, event):
        payload = {"secret_chat_id": event.chat_id, "peer_user_id": self.peer(event.chat_id), "direction": "in",
                   "random_id": event.random_id, "seq_no": event.seq_no, "text": event.text, "ttl": event.ttl,
                   "reply_to_random_id": event.reply_to,
                   "entities": plain(event.entities) if event.entities else None,
                   "media": plain(event.media) if event.media is not None else None}
        mark = fingerprint(payload)
        key = (event.chat_id, event.random_id, mark)
        name = str(event.chat_id) + ":" + str(event.random_id)
        item = None
        if event.media_reference is not None and not self.has_file(event.chat_id, event.random_id,
                                                                    self.matching(payload)[0]):
            pending = self.collector.vault.read(PENDING) or {}
            name = slot(pending, name, mark, "message")
            item = pending.get(name) or encode({"secret_chat_id": event.chat_id, "random_id": event.random_id,
                                                "reference": event.media_reference.to_dict(), "message": payload})
            pending[name] = item
            self.collector.vault.save(PENDING, pending)
        try:
            if key not in self.seen:
                self.write_message(payload)
        except Exception:
            try:
                if item is None:
                    self.hold(name, payload)
            finally:
                if running():
                    self.resume_files()
            raise
        if len(self.seen) >= 4096:
            self.seen.clear()
        self.seen.add(key)
        if item is not None:
            self.save_later(item)

    def on_ServiceActionReceived(self, event):
        if event.action_name in QUIET:
            return
        if event.action_name == "DecryptedMessageActionTyping":
            return self.peer_typing(event.chat_id, getattr(event.action, "action", None))
        opened = event.action_name == "DecryptedMessageActionReadMessages"
        self.note("action", {"secret_chat_id": event.chat_id, "peer_user_id": self.peer(event.chat_id),
                             "action": event.action_name.removeprefix("DecryptedMessageAction"),
                             "details": plain(event.action), "applied_by_tgwitness": event.applied,
                             **({"random_ids": list(getattr(event.action, "random_ids", None) or []),
                                 "contents_opened": True} if opened else {}),
                             "meaning": PEER_OPENED_MEANING if opened else
                             "Reported by the other side. TgWitness keeps every earlier message."})

    def peer_typing(self, chat_id, action=None):
        from . import visibility
        if not settings(self.store)["enabled"]:
            return None
        return visibility.of(self.collector).peer_typing(chat_id, self.peer(chat_id), action, secret=True)

    def peer_read(self, update):
        if not settings(self.store)["enabled"]:
            return None
        max_date, read_at = unix(update.max_date), unix(update.date)
        return self.note("peer_read", {"secret_chat_id": update.chat_id, "peer_user_id": self.peer(update.chat_id),
                                       "max_date": max_date, "max_date_at": moment(max_date), "read_at": moment(read_at),
                                       "contents_opened": False, "meaning": PEER_READ_MEANING})

    def on_DecryptFailed(self, event):
        self.note("decrypt_failed", {"secret_chat_id": event.chat_id, "reason": event.reason})

    def on_SendFailed(self, event):
        self.note("send_failed", {"secret_chat_id": event.chat_id, "random_id": event.random_id, "cause": event.cause})

    def spawn(self, coroutine):
        task = asyncio.get_running_loop().create_task(coroutine)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return task

    def save_later(self, item):
        return self.resume_files()

    def resume_files(self):
        self.file_wakeup.set()
        if self.manager is not None and (self.file_worker is None or self.file_worker.done()):
            if self.collector.vault.read(PENDING) or self.collector.vault.read(HELD):
                self.file_worker = self.spawn(self.drain_files())
        return self.file_worker

    async def drain_files(self):
        while self.manager is not None:
            try:
                if not await self.next_file():
                    return
            except asyncio.CancelledError:
                raise
            except Exception:
                LOG.exception("The secret-chat attachment queue could not be updated")
                await asyncio.sleep(5)

    async def next_file(self):
        self.file_wakeup.clear()
        held = self.write_held()
        pending = self.collector.vault.read(PENDING) or {}
        if not pending and not held:
            return False
        if pending:
            name, item = min(pending.items(), key=lambda row: row[1].get("retry_at", 0))
            delay = min(300, max(0, item.get("retry_at", 0) - time.time()))
        else:
            name, delay = None, 30
        if held and delay:
            delay = min(delay, 30)
        if delay:
            try:
                await asyncio.wait_for(self.file_wakeup.wait(), delay)
            except TimeoutError:
                pass
            return True
        self.downloads[name] = asyncio.current_task()
        try:
            await self.save_file(decode(item), name)
        except asyncio.CancelledError:
            raise
        except Exception:
            LOG.exception("A pending secret-chat attachment could not be saved")
        finally:
            self.downloads.pop(name, None)
        pending = self.collector.vault.read(PENDING) or {}
        if name in pending:
            retries = min(7, pending[name].get("retries", 0) + 1)
            pending[name] = {**pending[name], "retries": retries,
                             "retry_at": time.time() + min(300, 5 * 2**(retries - 1))}
            self.collector.vault.save(PENDING, pending)
        return True

    def unaffordable(self, reference, media_root):
        capture = capture_settings(self.store)
        if not capture["download_media"]:
            return "attachment downloads are off"
        size = getattr(reference, "size", None)
        if not isinstance(size, int):
            size = None
        limit = capture["max_media_mb"] * 1024**2
        if size is not None and size > limit:
            return "larger than the media size limit"
        free = shutil.disk_usage(media_root).free
        if free - (size or 0) < self.collector.param("media_min_free_mb") * 1024**2:
            return "not enough free disk space"
        return None

    async def save_file(self, item, name=None):
        name = name or str(item["secret_chat_id"]) + ":" + str(item["random_id"])
        media_root = self.store.root / "media"
        media_root.mkdir(exist_ok=True)
        temporary = media_root / (".secret-" + secrets.token_hex(8))
        try:
            message = self.write_message(item["message"]) if item.get("message") else None
            if self.has_file(item["secret_chat_id"], item["random_id"], message):
                pending = self.collector.vault.read(PENDING) or {}
                if pending.pop(name, None) is not None:
                    self.collector.vault.save(PENDING, pending)
                return
            reference = library.MediaReference.from_dict(item["reference"])
            refused = self.unaffordable(reference, media_root)
            if refused:
                self.note("file_deferred", {"secret_chat_id": item["secret_chat_id"], "random_id": item["random_id"],
                                            "reason": refused,
                                            "meaning": "The encrypted file stays queued; nothing was downloaded."})
                return
            size = getattr(reference, "size", 0)
            size = max(0, size) if isinstance(size, int) else 0
            timeout = self.collector.param("media_timeout_seconds") + size // (self.collector.param("media_min_speed_kbps") * 1024)
            await asyncio.wait_for(self.manager.save_file(reference, temporary), timeout)
            digest, size, repaired = await complete_in_thread(retain_file, temporary, media_root)
            self.note("file", {"secret_chat_id": item["secret_chat_id"], "random_id": item["random_id"],
                               **({"message_event": message} if message else {}),
                               "media_sha256": digest, "size": size,
                               **({"cache_repair": repaired} if repaired else {}),
                               "meaning": "Decrypted by TgWitness and stored by its SHA-256; the message record describes it."})
        except asyncio.CancelledError:
            temporary.unlink(missing_ok=True)
            raise
        except Exception as exc:
            temporary.unlink(missing_ok=True)
            self.note("file_failed", {"secret_chat_id": item["secret_chat_id"], "random_id": item["random_id"],
                                      "error_type": type(exc).__name__})
            return
        pending = self.collector.vault.read(PENDING) or {}
        if pending.pop(name, None) is not None:
            self.collector.vault.save(PENDING, pending)

    async def acting(self, call, *args, **kwargs):
        from . import interactions
        interactions.permitted(self.collector)
        try:
            return await call(*args, **kwargs)
        except Exception as exc:
            interactions.note_restriction(self.store, exc)
            raise

    async def create(self, user):
        manager = self.require()
        client = self.collector.client
        try:
            entity = await client.get_input_entity(user)
        except ValueError:
            if not isinstance(user, int):
                raise ValueError("Telegram has no user with this username.") from None
            await self.collector.dialogs()
            try:
                entity = await client.get_input_entity(user)
            except ValueError:
                raise ValueError("This account does not know that user ID yet. Use the @username, "
                                 "or open a chat with the user first.") from None
        if not isinstance(utils.get_peer(entity), types.PeerUser):
            raise ValueError("This needs a Telegram user, not a group or channel.")
        chat = await self.acting(manager.create, entity)
        self.note("requested", {"secret_chat_id": chat.id, "peer_user_id": chat.peer_user_id, "direction": "out"})
        return self.snapshot(chat)

    async def accept(self, chat_id, automatic=False):
        manager = self.require()
        if automatic and not settings(self.store)["accept_incoming"]:
            self.note("accept_failed", {"secret_chat_id": chat_id, "automatic": True,
                                        "reason": "accept_incoming turned off"})
            return None
        try:
            chat = await self.acting(manager.accept, chat_id)
        except Exception as exc:
            self.note("accept_failed", {"secret_chat_id": chat_id, "automatic": automatic,
                                        "reason": str(exc) if isinstance(exc, ValueError) else type(exc).__name__})
            if automatic:
                return None
            raise
        self.note("accepted", {"secret_chat_id": chat_id, "peer_user_id": chat.peer_user_id,
                               "automatic": automatic,
                               "meaning": "This chat now lives in TgWitness; other devices of the account do not get it."})
        return self.snapshot(chat)

    async def send(self, chat_id, text):
        from . import interactions, visibility
        manager = self.require()
        fields, typing = visibility.effective(self.store, chat_id, True), None
        if fields["typing"] == "before_send":
            interactions.permitted(self.collector)
            typing = await visibility.show_typing(self.collector, "secret_chat.typing", {
                "secret_chat_id": chat_id, "peer_user_id": self.peer(chat_id), "method": "messages.setEncryptedTyping"},
                functions.messages.SetEncryptedTypingRequest(self.input_chat(chat_id), True),
                visibility.typing_seconds(text))
        random_id = await self.acting(manager.send_message, chat_id, text)
        chat = manager.status(chat_id)
        sent = self.note("message", {"secret_chat_id": chat_id, "peer_user_id": chat.peer_user_id, "direction": "out",
                                     "random_id": random_id, "text": text, "ttl": chat.ttl,
                                     **({"typing_before_send": typing} if typing else {})})
        if fields["read_receipts"] == "on_reply":
            try:
                await self.mark_read(chat_id, "on_reply", cause={
                    "after_panel_action": {"action": "send", "message_event": sent["seq"]}})
            except Exception as exc:
                LOG.info("No read receipt after the panel message in secret chat %s: %s", chat_id, type(exc).__name__)
        return random_id

    def input_chat(self, chat_id):
        chat = self.require()._entity(chat_id)
        return types.InputEncryptedChat(chat.id, chat.access_hash)

    def received(self, chat_id, random_ids=None):
        query = ("SELECT json_extract(payload,'$.random_id'), max(observed_at), max(json_extract(payload,'$.ttl')), "
                 "max(json_extract(payload,'$.media._')) FROM events WHERE kind='secret_chat.message' "
                 "AND json_extract(payload,'$.secret_chat_id')=? AND json_extract(payload,'$.direction')='in'")
        values = [chat_id]
        if random_ids is not None:
            query += " AND json_extract(payload,'$.random_id') IN (" + ",".join("?" * len(random_ids)) + ")"
            values += list(random_ids)
        with self.store.lock:
            return self.store.db.execute(query + " GROUP BY 1 ORDER BY 2 DESC", values).fetchall()

    def unopened(self, chat_id):
        from . import visibility
        opened = set(visibility.marks(self.store).get("opened:" + visibility.mark_key(chat_id, True)) or [])
        return [{"random_id": str(row[0]), "observed_at": row[1], "ttl": row[2], "media": row[3]}
                for row in self.received(chat_id) if (row[2] or row[3]) and row[0] not in opened][:20]

    def definite(self):
        return tuple(error for error in (getattr(library, name, None) for name in ("ChatClosed", "ChatNotReady",
                                                                                     "UnknownChat"))
                     if isinstance(error, type))

    async def mark_read(self, chat_id, trigger, operator=None, cause=None):
        from . import interactions, visibility
        visibility.require(self.store, chat_id, True, "read_receipts", trigger)
        interactions.permitted(self.collector)
        self.require()
        newest = max((row[1] for row in self.received(chat_id)), default=None)
        if newest is None:
            raise ValueError("No received message of this chat is saved here, so nothing can be marked as read.")
        bound, key = int(datetime.fromisoformat(newest).timestamp()), visibility.mark_key(chat_id, True)
        done = visibility.marks(self.store).get(key)
        if isinstance(done, int) and done >= bound:
            return {"status": "unchanged", "secret_chat_id": chat_id, "max_date": done, "trigger": trigger}
        request = functions.messages.ReadEncryptedHistoryRequest(self.input_chat(chat_id), bound)
        details = {"secret_chat_id": chat_id, "peer_user_id": self.peer(chat_id), "trigger": trigger, "max_date": bound,
                   "max_date_at": moment(bound), "covers": "received messages dated up to this time",
                   "method": "messages.readEncryptedHistory", **visibility.operator_of(operator), **(cause or {}),
                   "meaning": READ_MEANING}
        result = await visibility.dispatch(self.collector, "secret_chat.read", details, lambda: self.client(request),
                                           None, (type(request), chat_id, bound), self.definite())
        if result["status"] == "succeeded":
            visibility.remember(self.store, key, bound)
            await visibility.opsec.hide_presence(self.collector, result["request_event"])
        return {**result, "secret_chat_id": chat_id, "max_date": bound, "trigger": trigger}

    async def mark_opened(self, chat_id, random_ids, operator=None):
        from . import interactions, visibility
        visibility.require(self.store, chat_id, True, "content_opened", "manual")
        interactions.permitted(self.collector)
        manager = self.require()
        ids = sorted(set(random_ids))
        if set(ids) - {row[0] for row in self.received(chat_id, ids)}:
            raise ValueError("Only received messages saved here can be marked as opened.")
        details = {"secret_chat_id": chat_id, "peer_user_id": self.peer(chat_id), "trigger": "manual", "random_ids": ids,
                   "method": "messages.sendEncryptedService", "service_action": "DecryptedMessageActionReadMessages",
                   **visibility.operator_of(operator), "meaning": CONTENT_MEANING}
        result = await visibility.dispatch(self.collector, "secret_chat.contents", details,
                                           lambda: manager.mark_read(chat_id, ids), None, None, self.definite())
        if result["status"] == "succeeded":
            key = "opened:" + visibility.mark_key(chat_id, True)
            done = set(visibility.marks(self.store).get(key) or []) | set(ids)
            visibility.remember(self.store, key, sorted(done)[-visibility.OPENED_LIMIT:])
            await visibility.opsec.hide_presence(self.collector, result["request_event"])
        return {**result, "secret_chat_id": chat_id, "random_ids": [str(value) for value in ids]}

    async def send_typing(self, chat_id, operator=None):
        from . import interactions, visibility
        visibility.require(self.store, chat_id, True, "typing", "shown")
        interactions.permitted(self.collector)
        self.require()
        request = functions.messages.SetEncryptedTypingRequest(self.input_chat(chat_id), True)
        return await visibility.of(self.collector).ping(("secret", chat_id), "secret_chat.typing", {
            "secret_chat_id": chat_id, "peer_user_id": self.peer(chat_id), "mode": "shown",
            "method": "messages.setEncryptedTyping", **visibility.operator_of(operator)}, request)

    async def close(self, chat_id):
        manager = self.require()
        await self.acting(manager.close, chat_id, reason="ended from TgWitness")

    @staticmethod
    def snapshot(chat):
        return {"id": chat.id, "state": getattr(chat.state, "name", str(chat.state)).lower(),
                "peer_user_id": chat.peer_user_id, "outbound": chat.is_outbound, "ttl": chat.ttl, "layer": chat.layer,
                "key_visualization": library.key_visualization(chat.key_hash).hex if chat.key_hash else None,
                "created_at": chat.created_at, "closed_reason": chat.closed_reason}

    def person(self, user_id):
        collector = self.collector
        entity = collector.people.get(user_id) or collector.dialog_cache.get(user_id, {}).get("entity")
        if entity is not None:
            return {"name": utils.get_display_name(entity) or None, "username": getattr(entity, "username", None)}
        if user_id not in self.asked and self.client is not None and running():
            self.asked.add(user_id)
            self.spawn(self.learn(user_id))
        return None

    async def learn(self, user_id):
        try:
            entity = await self.client.get_entity(types.PeerUser(user_id))
        except Exception:
            return
        self.collector.people[utils.get_peer_id(entity)] = entity

    def view(self, *, before=None, after=None):
        from . import interactions
        interaction_problem = None
        try:
            interactions.permitted(self.collector)
        except (ValueError, FloodWaitError) as exc:
            interaction_problem = str(exc)
        connected = self.manager is not None and self.client is not None and self.client.is_connected()
        chats = [self.snapshot(chat) for chat in self.manager.list()] if self.manager is not None else []
        if before is not None and after is not None:
            raise ValueError("Choose an older or newer history page, not both.")
        records = self.store.events(kind="secret_chat.", limit=2001, before=before, after=after)
        more = len(records) > 2000
        if after is not None:
            records.reverse()
        records = records[:2000]
        if after is None:
            records.reverse()
        return {"available": available(), "settings": settings(self.store), "connected": connected, "error": self.error,
                "has_session": bool((self.collector.vault.read("credentials") or {}).get("session")),
                "interaction_problem": interaction_problem,
                "interaction_goal": interaction_problem == interactions.GOAL_OFF,
                "module": secret_module.describe(),
                "chats": display(sorted(chats, key=lambda chat: chat["created_at"] or 0, reverse=True)),
                "people": {str(user_id): self.person(user_id) for user_id in
                           {chat["peer_user_id"] for chat in chats if type(chat["peer_user_id"]) is int}},
                "records": display(records),
                "next_before": records[0]["seq"] if more and after is None else None,
                "next_after": records[-1]["seq"] if more and after is not None else None,
                "pending_files": len(self.collector.vault.read(PENDING) or {}),
                "unavailable_reason": None if available() else UNAVAILABLE}
