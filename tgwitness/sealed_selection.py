import hashlib
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .account_export import AccountExportOptions
from .monitoring import Capture, normalize_capture
from .store import canonical

MAX_CHAT_EXPORTS = 50
# A @username, a numeric user ID from this account's chats, or an international phone number.
SECRET_PEER = r"^(@?[A-Za-z][A-Za-z0-9_]{3,31}|[0-9]{1,20}|\+[0-9]{7,15})$"


def secret_target(value):
    value = value.removeprefix("@")
    return int(value) if value.isdigit() else value


class SecretVisibility(BaseModel):
    """What the other side of a captured secret chat may see. The default sends nothing: no read receipts, no
    opened notices for self-destructing content, no typing. Downloading and viewing files never notifies anyone."""
    model_config = ConfigDict(extra="forbid")
    # on_open: the panel marks messages read a few seconds after they appear while the panel is in view.
    read_receipts: Literal["never", "manual", "on_reply", "on_open"] = "never"
    content_opened: Literal["never", "manual"] = "never"
    typing: Literal["hidden", "shown", "before_send"] = "hidden"


class Selection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["chat", "account", "chats", "secret"] = "chat"
    chat_id: int | None = Field(default=None, strict=True)
    # Pseudo-secret capture: start a secret chat with this user, accept ones the other side starts, or both.
    secret_peer: str | None = Field(default=None, pattern=SECRET_PEER)
    accept_incoming: bool | None = None
    secret_visibility: SecretVisibility | None = None
    # Investigation export: each chat becomes its own signed chat export inside the sealed archive, in this order.
    chat_ids: list[int] | None = Field(default=None, min_length=1, max_length=MAX_CHAT_EXPORTS)
    capture: Capture = Field(default_factory=lambda: Capture.model_validate({
        **normalize_capture(None), "include_avatars": False, "messages_first": True}))
    account_scope: Literal["all", "selected"] | None = None
    account_options: AccountExportOptions | None = None

    @model_validator(mode="after")
    def scope(self):
        if self.mode != "chats" and self.chat_ids is not None:
            raise ValueError("Chat lists belong to the chat investigation export.")
        if self.mode != "secret" and (self.secret_peer is not None or self.accept_incoming is not None
                                      or self.secret_visibility is not None):
            raise ValueError("Secret chat settings belong to the secret chat capture.")
        if self.mode == "secret":
            if self.chat_id is not None or self.account_options is not None or self.account_scope is not None:
                raise ValueError("A secret chat capture takes no chat or account selection.")
            self.accept_incoming = True if self.accept_incoming is None else self.accept_incoming
            if self.secret_peer is not None:
                self.secret_peer = self.secret_peer.removeprefix("@")
            if self.secret_peer is None and not self.accept_incoming:
                raise ValueError("Name the user to start a secret chat with, or accept secret chats started by others.")
        elif self.mode == "chats":
            if (self.chat_id is not None or self.account_options is not None or self.account_scope is not None
                    or not self.chat_ids):
                raise ValueError("Select one or more chats for the investigation export.")
            if any(type(c) is not int or c == 0 or not -(2**63) < c < 2**63 for c in self.chat_ids):
                raise ValueError("Chat IDs must be nonzero 64-bit integers.")
            if len(set(self.chat_ids)) != len(self.chat_ids):
                raise ValueError("Each chat can be selected once.")
        elif self.mode == "chat":
            if self.chat_id is None or self.account_options is not None or self.account_scope is not None:
                raise ValueError("Select a chat and its capture settings.")
        else:
            if self.chat_id is not None or self.account_options is None or "capture" in self.model_fields_set:
                raise ValueError("Account export requires account_options, without chat capture settings.")
            if not self.account_options.messages_first:
                raise ValueError("Restricted account exports preserve messages before attachments.")
            inferred = "selected" if self.account_options.chat_ids else "all"
            if self.account_scope is not None and self.account_scope != inferred:
                raise ValueError("Selected scope requires chat IDs; all-chat scope must not restrict chat IDs.")
            self.account_scope = inferred
        return self

    def settings(self):
        if self.mode == "account":
            return {"mode": "account", "account_scope": self.account_scope,
                    "account_options": self.account_options.model_dump()}
        if self.mode == "chats":
            return {"mode": "chats", "chat_ids": list(self.chat_ids), "capture": normalize_capture(self.capture.model_dump())}
        if self.mode == "secret":
            return {"mode": "secret", "secret_peer": self.secret_peer, "accept_incoming": self.accept_incoming,
                    "capture": normalize_capture(self.capture.model_dump()),
                    # Absent in archives made before this choice existed; they keep their original digest.
                    **({"secret_visibility": self.secret_visibility.model_dump()} if self.secret_visibility else {})}
        return {"mode": "chat", "chat_id": self.chat_id, "capture": normalize_capture(self.capture.model_dump())}


def selection_hash(settings):
    return hashlib.sha256(canonical(settings)).hexdigest()


def checked_selection(events, internal, expected=None, require_complete=False):
    if len(events) != 1:
        raise ValueError("Expected exactly one signed capture selection")
    event = events[0]
    if event.get("mode") == "account":
        raw = {"mode": "account", "account_options": event.get("options")}
    elif event.get("mode") == "chats":
        raw = {"mode": "chats", "chat_ids": event.get("chat_ids"), "capture": event.get("capture")}
    elif event.get("mode") == "secret":
        raw = {"mode": "secret", "secret_peer": event.get("secret_peer"), "accept_incoming": event.get("accept_incoming"),
               "capture": event.get("capture"), "secret_visibility": event.get("secret_visibility")}
    else:
        raw = {"mode": "chat", "chat_id": event.get("chat_id"), "capture": event.get("capture")}
    settings = Selection.model_validate(raw).settings()
    digest = selection_hash(settings)
    transport = settings["account_options"]["transport"] if settings["mode"] == "account" else "regular"
    if event.get("transport") != transport:
        raise ValueError("Signed selection transport mismatch")
    if "selection" in event or "selection_sha256" in event:
        if event.get("selection") != settings or event.get("selection_sha256") != digest:
            raise ValueError("Signed selection digest mismatch")
    account = internal.get("account_export")
    if settings["mode"] == "account":
        if account is None or account.get("options") != settings["account_options"]:
            raise ValueError("Account export differs from the signed capture selection")
    elif account is not None:
        raise ValueError("Unexpected account export in a chat capture")
    chats = internal.get("chat_exports") or []
    if settings["mode"] != "chats" and chats:
        raise ValueError("Unexpected chat export in this capture")
    if any(item["chat_id"] not in settings.get("chat_ids", ()) for item in chats):
        raise ValueError("A chat export is outside the signed capture selection")
    if expected is not None and Selection.model_validate(expected).settings() != settings:
        raise ValueError("Capture settings differ from the independently expected selection")
    if settings["mode"] == "chats":
        complete = ([item["chat_id"] for item in chats if item["complete"]] == settings["chat_ids"])
        mode = "chat_export"
    elif settings["mode"] == "secret":
        complete, mode = None, "secret_chat"
    else:
        complete = account["complete_within_scope"] if account else None
        mode = transport if account else "journal"
    if require_complete and complete is not True:
        raise ValueError("A complete export within the selected scope is required")
    return {"selection": settings, "selection_sha256": digest, "mode": mode, "complete_within_scope": complete,
            "chat_exports": chats or None, "expected_selection_matched": True if expected is not None else None}
