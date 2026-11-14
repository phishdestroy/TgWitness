from .common import (
    Ed25519PublicKey,
    FIELDS,
    base64,
    hashlib,
    re,
    strict_json,
    validate_server_hashes,
)
class EventChain:
    def __init__(self, public_key, remember=None):
        self.public_key, self.remember, self.checks = public_key, remember, None
        self.key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key, validate=True))
        self.previous, self.count = "0" * 64, 0
        self.previous_time = self.previous_at = None
        self.chronology = {"regressions": 0, "unparseable": 0, "samples": []}

    def structure(self, event):
        count = self.count + 1
        if set(event) != set(FIELDS) | {"hash", "signature"}:
            raise ValueError("Unexpected or missing fields at event " + str(count))
        if event["seq"] != count or event["previous_hash"] != self.previous:
            raise ValueError("Broken sequence or hash chain at event " + str(count))

    def content(self, event):
        from .chain import canonical
        calculated = hashlib.sha256(canonical({k: event[k] for k in FIELDS})).hexdigest()
        if event["hash"] != calculated:
            raise ValueError("Changed content at event " + str(self.count + 1))
        self.key.verify(base64.b64decode(event["signature"], validate=True), bytes.fromhex(calculated))
        return calculated

    def settle(self, event, digest):
        from .coverage import parse_time
        count, chronology, anomaly = self.count + 1, self.chronology, None
        try:
            observed = parse_time(event["observed_at"])
            if observed.utcoffset() is None:
                raise ValueError("Observation time has no UTC offset")
        except (AttributeError, TypeError, ValueError, OverflowError):
            observed = None
            chronology["unparseable"] += 1
            anomaly = {"seq": count, "observed_at": event["observed_at"], "reason": "unparseable"}
        if observed is not None and self.previous_time is not None and observed < self.previous_time:
            chronology["regressions"] += 1
            anomaly = {"seq": count, "observed_at": event["observed_at"], "previous_at": self.previous_at,
                       "backwards_seconds": (self.previous_time - observed).total_seconds(), "reason": "regression"}
        if anomaly is not None and len(chronology["samples"]) < 100:
            chronology["samples"].append(anomaly)
        if observed is not None:
            self.previous_time, self.previous_at = observed, event["observed_at"]
        if event["kind"] == "media.hashed":
            payload = event["payload"]
            validate_server_hashes(payload.get("server_hashes"))
            if (payload["server_hashes"]["status"] != "complete" or payload.get("downloaded_bytes") != 0
                    or payload.get("media_sha256") is not None):
                raise ValueError("A hash-only record incorrectly claims downloaded file content")
        self.previous, self.count = digest, count
        if self.remember is not None and count in self.remember:
            self.remember[count] = digest

    def run(self, events):
        for event in events:
            self.structure(event)
            self.settle(event, self.content(event))
        return self.result()

    def run_lines(self, lines, take=None):
        from .parallel import PARALLEL_EVENTS_AFTER, JournalChecks, parallel_pool
        for line in lines:
            event = strict_json(line)
            try:
                if take is not None:
                    take(event)
                if self.checks is None and self.count >= PARALLEL_EVENTS_AFTER and parallel_pool() is not None:
                    self.checks = JournalChecks(self.public_key)
                self.structure(event)
                if self.checks is None:
                    digest = self.content(event)
                else:
                    self.checks.add(self.count + 1, line)
                    digest = event["hash"]
                self.settle(event, digest)
            except Exception:
                if self.checks is not None:
                    self.checks.settle()
                raise
        if self.checks is not None:
            self.checks.settle()
        return self.result()

    def result(self):
        from .chain import fingerprint
        result = {"events": self.count, "head_hash": self.previous, "fingerprint": fingerprint(self.public_key)}
        if self.chronology["regressions"] or self.chronology["unparseable"]:
            self.chronology["meaning"] = ("Observation times come from the collector's clock; the hash chain fixes the "
                                          "order of the records, and timestamps, drand rounds and witness records fix "
                                          "them in time. These entries do not affect the signatures.")
            result["chronology"] = self.chronology
        return result


def verify_events(events, public_key, remember=None):
    return EventChain(public_key, remember).run(events)


def verify_event_lines(lines, public_key, take=None, remember=None):
    return EventChain(public_key, remember).run_lines(lines, take)


def media_reference(event):
    if event["kind"] not in ("media.saved", "actor.avatar_saved", "secret_chat.file"):
        return None
    payload = event["payload"]
    digest, size = payload.get("media_sha256"), payload.get("size")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("Invalid media reference in the signed journal")
    if size is not None and (type(size) is not int or size < 0):
        raise ValueError("Invalid media size in the signed journal")
    return digest, size


def verify_checkpoint(checkpoint, public_key, event_count, hash_at, check_drand=False):
    from .chain import canonical, is_format
    from .outside import confirm_drand
    statement = checkpoint["statement"]
    if not is_format(statement["format"], "checkpoint-v1") or statement["public_key"] != public_key:
        raise ValueError("Checkpoint format or signing key mismatch")
    if type(statement["event_count"]) is not int or statement["event_count"] < 0:
        raise ValueError("Invalid checkpoint event count")
    Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key, validate=True)).verify(
        base64.b64decode(checkpoint["signature"], validate=True), canonical(statement))
    if statement["event_count"] > event_count:
        raise ValueError("Journal is shorter than the retained checkpoint")
    if hash_at(statement["event_count"]) != statement["head_hash"]:
        raise ValueError("Journal disagrees with the retained checkpoint")
    anchor = statement.get("drand_anchor")
    if check_drand and anchor and isinstance(anchor.get("round"), int) and isinstance(anchor.get("randomness"), str):
        try:
            confirmed = confirm_drand([{"round": anchor["round"], "randomness": anchor["randomness"],
                                        "seq": statement["event_count"]}])
        except ValueError as exc:
            raise ValueError("Checkpoint drand anchor: " + str(exc)) from exc
        if confirmed["confirmed"] == 0:
            raise ValueError("Checkpoint drand anchor round " + str(anchor["round"])
                             + " could not be confirmed against any drand relay")
    return anchor if anchor else None


