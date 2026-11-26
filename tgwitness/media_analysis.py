import asyncio
import hashlib
import importlib.metadata
import importlib.util
import json
import logging
import os
from pathlib import Path
import re
import secrets
import shutil
import sys
import tempfile
import threading
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .access import Refused
from .archive import ArchiveQuery
from .store import utcnow

LOG = logging.getLogger("tgwitness.media")
MAX_FILE = 50 * 1024 * 1024
MAX_SECONDS = 86400
_WHISPER_MODELS = {}
_WHISPER_LOCK = threading.Lock()


class MediaJob(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace: str = "default"
    chat_id: int
    event_seq: int = Field(ge=1)
    digest: str = Field(pattern=r"^[a-f0-9]{64}$")
    engine: Literal["ocr", "transcription"]
    language: str = Field(default="", pattern=r"^[a-z]{0,3}$")


class Segment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    start: float = Field(ge=0, le=MAX_SECONDS)
    end: float = Field(ge=0, le=MAX_SECONDS)
    text: str = Field(max_length=100000)

    @model_validator(mode="after")
    def ordered(self):
        if self.end < self.start:
            raise ValueError("The media worker returned an invalid result.")
        return self


class Recognition(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    text: str = Field(max_length=100000)
    engine: str = Field(min_length=1, max_length=80)
    engine_version: str = Field(min_length=1, max_length=160)
    model_version: str = Field(min_length=1, max_length=256)
    language: str = Field(max_length=20)
    segments: list[Segment] = Field(max_length=3000)
    parameters: dict[str, str | float | int | bool] = Field(max_length=20)


def container_available():
    image = os.environ.get("TGWITNESS_MEDIA_IMAGE", "")
    return bool(image and shutil.which("docker") and os.name == "posix")


def whisper_available():
    if os.environ.get("TGWITNESS_WHISPER_LOCAL", "1").strip().lower() in ("0", "false", "no", "off"):
        return False
    return importlib.util.find_spec("faster_whisper") is not None


def whisper_downloads(state):
    enabled = ("1", "true", "yes")
    if (os.environ.get("TGWITNESS_WHISPER_ALLOW_DOWNLOAD", "").strip().lower() not in enabled
            or os.environ.get("TGWITNESS_WHISPER_OFFLINE", "").strip().lower() in enabled
            or os.environ.get("TGWITNESS_WHISPER_MODEL_DIR", "").strip()):
        return False
    return state.collector.outside_route().kind == "direct"


def backend_for(engine):
    prefer_local = os.environ.get("TGWITNESS_WHISPER_BACKEND", "").strip().lower() == "local"
    if engine == "transcription":
        if prefer_local and whisper_available():
            return "local-whisper"
        if container_available():
            return "local-container"
        if whisper_available():
            return "local-whisper"
        return None
    if engine == "ocr":
        return "local-container" if container_available() else None
    return None


def available(engine=None):
    if engine is not None:
        return backend_for(engine) is not None
    return container_available() or whisper_available()


def capabilities():
    has_container = container_available()
    has_whisper = whisper_available()
    backends = []
    if has_container:
        backends.append("local-container")
    if has_whisper:
        backends.append("local-whisper")
    processing = "local-container" if has_container else ("local-whisper" if has_whisper else None)
    return {
        "available": has_container or has_whisper,
        "processing": processing,
        "backends": backends,
        "engines": {"ocr": has_container, "transcription": has_container or has_whisper},
    }


def docker():
    return ["docker", "--host", "unix://" + os.environ.get("TGWITNESS_DOCKER_SOCKET", "/var/run/docker.sock")]


def authorize(reader, job):
    state = reader.workspace(ArchiveQuery(tool="get_journal_event", workspace=job.workspace, chat_id=job.chat_id), chat=True)
    event = reader.read(ArchiveQuery(tool="get_journal_event", workspace=job.workspace,
                                    chat_id=job.chat_id, event_seq=job.event_seq))
    if event["media_sha256"] != job.digest or not state.store.media_in_chats(job.digest, {job.chat_id}):
        raise Refused("This attachment is unavailable to the selected chat.")
    path = state.store.root / "media" / job.digest
    if not path.is_file() or path.is_symlink() or path.stat().st_size > MAX_FILE:
        raise ValueError("Choose an available attachment of at most 50 MiB.")
    return state, path, event["source"]


def container_command(name, media, job):
    image = os.environ.get("TGWITNESS_MEDIA_IMAGE", "")
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._/:@-]{0,240}", image):
        raise ValueError("Configure a local media worker image on the server.")
    command = docker() + ["run", "--rm", "--pull=never", "--name", name, "--network=none", "--read-only",
               "--cap-drop=ALL", "--security-opt=no-new-privileges", "--pids-limit=64", "--cpus=1",
               "--memory=2g", "--memory-swap=2g", "--user=65534:65534", "--ulimit=nofile=128:128",
               "--tmpfs=/tmp:rw,noexec,nosuid,size=128m", "-e", "OMP_NUM_THREADS=1",
               "-e", "HF_HUB_OFFLINE=1", "-e", "TRANSFORMERS_OFFLINE=1",
               "--mount", "type=bind,src=" + str(media) + ",dst=/input/media,readonly"]
    if job.engine == "transcription":
        model = Path(os.environ.get("TGWITNESS_WHISPER_MODEL_DIR", "")).resolve()
        if not os.environ.get("TGWITNESS_WHISPER_MODEL_DIR") or not (model / "model.bin").is_file() or "," in str(model):
            raise ValueError("Install a local Whisper model and set TGWITNESS_WHISPER_MODEL_DIR.")
        command += ["--mount", "type=bind,src=" + str(model) + ",dst=/model,readonly"]
    return command + [image, job.engine, job.language]


async def tail(stream, limit):
    kept = b""
    while chunk := await stream.read(16384):
        kept = (kept + chunk)[-limit:]
    return kept


async def bounded(stream, limit):
    chunks, total = [], 0
    while chunk := await stream.read(16384):
        total += len(chunk)
        if total > limit:
            raise ValueError("The media worker output exceeded its limit.")
        chunks.append(chunk)
    return b"".join(chunks)


def _load_whisper_model(model_name, device, compute_type, model_dir, local_only):
    key = (model_name, device, compute_type, model_dir, local_only)
    with _WHISPER_LOCK:
        cached = _WHISPER_MODELS.get(key)
        if cached is not None:
            return cached
        from faster_whisper import WhisperModel
        kwargs = {"device": device, "compute_type": compute_type, "local_files_only": local_only}
        source = model_name
        if model_dir and (Path(model_dir) / "model.bin").is_file():
            source = model_dir
        elif model_dir:
            kwargs["download_root"] = model_dir
        try:
            model = WhisperModel(source, **kwargs)
        except OSError:
            if not local_only:
                raise
            raise ValueError("The local Whisper model is not installed. Copy a faster-whisper model folder with model.bin "
                             "to this server and set TGWITNESS_WHISPER_MODEL_DIR to it. Downloads are off; "
                             "TGWITNESS_WHISPER_ALLOW_DOWNLOAD=1 allows one only when requests outside Telegram use a "
                             "direct route.") from None
        _WHISPER_MODELS[key] = model
        return model


def _transcribe_sync(path, job, download=False):
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != job.digest:
        raise ValueError("The stored attachment does not match its saved hash.")
    model_name = os.environ.get("TGWITNESS_WHISPER_MODEL", "base").strip() or "base"
    model_dir = os.environ.get("TGWITNESS_WHISPER_MODEL_DIR", "").strip()
    device = os.environ.get("TGWITNESS_WHISPER_DEVICE", "cpu").strip() or "cpu"
    compute_type = os.environ.get("TGWITNESS_WHISPER_COMPUTE", "int8").strip() or "int8"
    local_only = not download
    model = _load_whisper_model(model_name, device, compute_type, model_dir, local_only)
    kwargs = {"beam_size": 5, "vad_filter": True}
    if job.language:
        kwargs["language"] = job.language
    raw_segments, info = model.transcribe(str(path), **kwargs)
    segments = []
    parts = []
    total_chars = 0
    truncated = False
    for seg in raw_segments:
        text = str(getattr(seg, "text", "") or "").strip()
        if not text:
            continue
        start = max(0.0, float(getattr(seg, "start", 0.0)))
        end = max(start, float(getattr(seg, "end", start)))
        remaining = 100000 - total_chars
        if len(segments) >= 3000 or remaining <= 0 or end > MAX_SECONDS:
            truncated = True
            break
        if len(text) > remaining:
            text = text[:remaining]
            truncated = True
        segments.append({"start": round(start, 3), "end": round(end, 3), "text": text})
        parts.append(text)
        total_chars += len(text) + 1
    try:
        version = importlib.metadata.version("faster-whisper")
    except importlib.metadata.PackageNotFoundError:
        version = "installed"
    detected_lang = str(getattr(info, "language", "") or job.language or "")[:20]
    full_text = "\n".join(parts)[:100000]
    payload = {
        "text": full_text,
        "engine": "faster-whisper",
        "engine_version": str(version)[:160],
        "model_version": model_name[:256],
        "language": detected_lang,
        "segments": segments,
        "parameters": {"device": device, "compute_type": compute_type, "vad_filter": True, "local_files_only": local_only,
                       "truncated": truncated},
    }
    return Recognition.model_validate(payload).model_dump()


async def run_local_whisper(path, job, download=False):
    if not whisper_available():
        raise ValueError("Local Whisper transcription requires faster-whisper. Install tgwitness[whisper].")
    env = dict(os.environ)
    if not download:
        env.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1")
    package_root = str(Path(__file__).resolve().parents[1])
    env["PYTHONPATH"] = os.pathsep.join(filter(None, (package_root, env.get("PYTHONPATH"))))
    process = await asyncio.create_subprocess_exec(
        sys.executable, "-P", "-m", "tgwitness.media_analysis", str(path), job.model_dump_json(),
        "download" if download else "offline", stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env, cwd=package_root)
    try:
        async with asyncio.timeout(300):
            output, errors = await asyncio.gather(bounded(process.stdout, 4 * 1024 * 1024), tail(process.stderr, 4096))
            code = await process.wait()
    finally:
        if process.returncode is None:
            process.kill()
            await process.wait()
    if code not in (0, 3) and errors:
        LOG.warning("Local Whisper worker exited with %s: %s", code, errors.decode("utf-8", "replace").strip()[-1000:])
    if code == 3:
        try:
            message = str(json.loads(output)["error"])[:300]
        except (ValueError, KeyError, TypeError):
            message = ""
        if message:
            raise ValueError(message)
    if code != 0:
        raise ValueError("Local Whisper transcription failed. Check the file format and the local model.")
    try:
        return Recognition.model_validate_json(output).model_dump()
    except ValueError:
        raise ValueError("The media worker returned an invalid result.") from None


async def run_container(path, job, ident):
    if not container_available():
        raise ValueError("Local media processing requires the configured Linux container worker.")
    name = "tgw-media-" + ident
    with tempfile.TemporaryDirectory(prefix="tgw-media-") as temp:
        media = Path(temp) / "media"
        await asyncio.to_thread(shutil.copyfile, path, media)
        media.chmod(0o444)
        with media.open("rb") as stream:
            digest = await asyncio.to_thread(lambda: hashlib.file_digest(stream, "sha256").hexdigest())
        if digest != job.digest:
            raise ValueError("The stored attachment does not match its saved hash.")
        process = await asyncio.create_subprocess_exec(*container_command(name, media, job),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        try:
            async with asyncio.timeout(300):
                output, _ = await asyncio.gather(bounded(process.stdout, 1024 * 1024), bounded(process.stderr, 16384))
                if await process.wait() != 0:
                    raise ValueError("Local media processing failed. Check the worker image, file format and model.")
                try:
                    return Recognition.model_validate_json(output).model_dump()
                except ValueError:
                    raise ValueError("The media worker returned an invalid result.") from None
        finally:
            if process.returncode is None:
                process.kill()
                await process.wait()
            cleanup = await asyncio.create_subprocess_exec(*docker(), "rm", "-f", name,
                stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
            try:
                await asyncio.wait_for(cleanup.wait(), 10)
            except TimeoutError:
                cleanup.kill()
                await cleanup.wait()


class MediaQueue:
    def __init__(self):
        self.slots = asyncio.Semaphore(1)
        self.tasks = {}

    def recover(self, state):
        entries = state.store.get_setting("media_analysis_jobs", [])
        changed = False
        for entry in entries:
            if entry["status"] in ("queued", "running") and entry["id"] not in self.tasks:
                entry.update(status="interrupted", error="Processing stopped before completion.")
                changed = True
        if changed:
            state.store.set_setting("media_analysis_jobs", entries)
        return entries

    @staticmethod
    def update(state, ident, **values):
        entries = state.store.get_setting("media_analysis_jobs", [])
        for entry in entries:
            if entry["id"] == ident:
                entry.update(values)
        state.store.set_setting("media_analysis_jobs", entries)

    def start(self, reader, job, owner, retry_of=None):
        state, path, source = authorize(reader, job)
        backend = backend_for(job.engine)
        if not backend:
            if job.engine == "transcription":
                raise ValueError("Transcription requires either the Linux container worker or faster-whisper (pip install tgwitness[whisper]).")
            raise ValueError("OCR requires the configured Linux container worker.")
        entries = self.recover(state)
        if len(self.tasks) >= 20 or len(entries) >= 100:
            raise ValueError("The media processing queue or result limit has been reached.")
        ident = secrets.token_hex(16)
        entry = {"id": ident, "owner": owner, "request": job.model_dump(), "source": source,
                 "created_at": utcnow(), "status": "queued", "error": None, "retry_of": retry_of,
                 "processing": backend}
        entries.append(entry)
        state.store.set_setting("media_analysis_jobs", entries)

        async def work():
            try:
                async with self.slots:
                    authorize(reader, job)
                    self.update(state, ident, status="running")
                    if backend == "local-whisper":
                        result = await run_local_whisper(path, job, whisper_downloads(state))
                        limits = {"timeout_seconds": 300}
                    else:
                        result = await run_container(path, job, ident)
                        limits = {"cpu": 1, "memory_mib": 2048, "timeout_seconds": 300}
                    artifact = {"schema": "tgwitness.media-analysis/1", "id": ident, "media_sha256": job.digest,
                                "source": source, "completed_at": utcnow(), "machine_recognition": True,
                                "processing": backend, "limits": limits, **{k: result[k] for k in ("text", "engine", "engine_version",
                                "model_version", "language", "segments", "parameters")}}
                    state.vault.save("media-analysis-" + ident, artifact)
                    self.update(state, ident, status="completed", completed_at=artifact["completed_at"])
            except asyncio.CancelledError:
                self.update(state, ident, status="cancelled")
                raise
            except Exception as exc:
                text = str(exc) if isinstance(exc, (ValueError, Refused)) else "Local processing stopped: " + type(exc).__name__
                self.update(state, ident, status="failed", error=text[:300])
            finally:
                self.tasks.pop(ident, None)
        self.tasks[ident] = asyncio.create_task(work())
        return entry

    async def cancel(self, ident, state):
        task = self.tasks.get(ident)
        if task:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
        self.update(state, ident, status="cancelled")
        self.tasks.pop(ident, None)

    async def close(self):
        tasks = list(self.tasks.values())
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        self.tasks.clear()


def main(argv):
    output = os.fdopen(os.dup(1), "w", encoding="utf-8")
    os.dup2(2, 1)
    try:
        result = _transcribe_sync(Path(argv[0]), MediaJob.model_validate_json(argv[1]), argv[2] == "download")
    except ValueError as exc:
        output.write(json.dumps({"error": str(exc)}))
        output.close()
        return 3
    output.write(json.dumps(result, ensure_ascii=False))
    output.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
