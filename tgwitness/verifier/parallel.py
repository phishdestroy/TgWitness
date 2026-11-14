from .common import (
    FIELDS,
    Ed25519PublicKey,
    InvalidSignature,
    base64,
    hashlib,
    member_digest,
    os,
    strict_json,
    zipfile,
)
PARALLEL = {"jobs": 1, "executor": None}
PARALLEL_JOBS_LIMIT = 16
PARALLEL_EVENTS_AFTER = 5000
PARALLEL_EVENT_BATCH = 2000
PARALLEL_HASH_BYTES = 64 * 1024**2


def parallel_jobs(value=None):
    if value is not None:
        jobs = (os.cpu_count() or 1) if value == "auto" else int(value)
        if jobs < 1:
            raise ValueError("--jobs needs a positive number or auto")
        PARALLEL["jobs"] = min(jobs, PARALLEL_JOBS_LIMIT)
    return PARALLEL["jobs"]


def parallel_pool():
    if PARALLEL["jobs"] < 2:
        return None
    if PARALLEL["executor"] is None:
        import concurrent.futures
        import multiprocessing
        PARALLEL["executor"] = concurrent.futures.ProcessPoolExecutor(
            PARALLEL["jobs"], mp_context=multiprocessing.get_context("spawn"))
    return PARALLEL["executor"]


def parallel_shutdown():
    executor, PARALLEL["executor"] = PARALLEL["executor"], None
    if executor is not None:
        executor.shutdown(wait=True, cancel_futures=True)


def journal_batch(public_key, first, lines):
    from .chain import canonical
    key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key, validate=True))
    for seq, line in enumerate(lines, first):
        try:
            event = strict_json(line)
            calculated = hashlib.sha256(canonical({k: event[k] for k in FIELDS})).hexdigest()
        except (ValueError, KeyError, TypeError):
            return seq, "content"
        if event["hash"] != calculated:
            return seq, "content"
        try:
            key.verify(base64.b64decode(event["signature"], validate=True), bytes.fromhex(calculated))
        except (InvalidSignature, ValueError, TypeError):
            return seq, "signature"
    return None


def journal_failure(found):
    seq, reason = found
    if reason == "signature":
        raise InvalidSignature("Invalid signature at event " + str(seq))
    raise ValueError("Changed content at event " + str(seq))


class JournalChecks:
    def __init__(self, public_key):
        self.public_key, self.pending, self.first, self.lines = public_key, [], None, []
        self.pool = parallel_pool()

    def add(self, seq, line):
        if not self.lines:
            self.first = seq
        self.lines.append(line)
        if len(self.lines) >= PARALLEL_EVENT_BATCH:
            self.submit()

    def submit(self):
        if self.lines:
            self.pending.append(self.pool.submit(journal_batch, self.public_key, self.first, self.lines))
            self.lines = []
        while len(self.pending) > 3 * PARALLEL["jobs"]:
            found = self.pending.pop(0).result()
            if found:
                self.abandon()
                journal_failure(found)

    def settle(self):
        self.submit()
        pending, self.pending = self.pending, []
        for index, future in enumerate(pending):
            found = future.result()
            if found:
                for rest in pending[index + 1:]:
                    rest.cancel()
                journal_failure(found)

    def abandon(self):
        for future in self.pending:
            future.cancel()
        self.pending, self.lines = [], []


def member_hashes(path, names):
    found = {}
    with zipfile.ZipFile(path) as archive:
        for name in names:
            digest = hashlib.sha256()
            with archive.open(name) as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            found[name] = digest.hexdigest()
    return found


class MemberHashes:
    def __init__(self, archive, path, names):
        self.archive, self.names, self.futures = archive, list(names), []
        sizes = {info.filename: info.compress_size for info in archive.infolist()}
        pool = parallel_pool() if isinstance(path, (str, os.PathLike)) else None
        if pool is None or len(self.names) < 2 or sum(sizes.get(n, 0) for n in self.names) < PARALLEL_HASH_BYTES:
            return
        buckets = [[0, []] for _ in range(2 * PARALLEL["jobs"])]
        for name in sorted(self.names, key=lambda n: -sizes.get(n, 0)):
            bucket = min(buckets, key=lambda b: b[0])
            bucket[0] += sizes.get(name, 0) + 4096
            bucket[1].append(name)
        self.futures = [pool.submit(member_hashes, os.fspath(path), names) for _, names in buckets if names]

    def result(self):
        if not self.futures:
            return {name: member_digest(self.archive, name) for name in self.names}
        found = {}
        for future in self.futures:
            found.update(future.result())
        self.futures = []
        return found

    def cancel(self):
        for future in self.futures:
            future.cancel()
        self.futures = []
