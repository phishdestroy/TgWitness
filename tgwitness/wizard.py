"""Step-by-step setup (the panel's /setup pages): one goal, the answers given so far and what applying
them changes.

The wizard is a front over the existing settings. Its progress is kept in the workspace, so a closed tab
returns to the same step. Applying writes the same scope, chats, recording, attachment and evidence
settings, with the same signed journal records, as their own forms; nothing here talks to Telegram.
"""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool

from . import levels
from .monitoring import MEDIA_DEFAULT_MB, MEDIA_TYPES
from .scope import EXCLUDE_LIMIT, SourceTypes

STEPS = ("goal", "connection", "account", "chats", "saving", "place", "summary")
# Saving a copy of the account is a one-off export: no chats to observe, nothing to keep running.
COPY_STEPS = ("goal", "connection", "account", "summary")
GOALS = ("copy", "watch", "evidence")
PURPOSES = ("personal", "investigation")
MEDIA = ("none", "small", "standard", "all")
HISTORY = ("none", "recent", "all")
RECENT_MESSAGES = 100
SMALL_MEDIA_MB = 20
NEW_CHATS = {"personal": {"profile": False, "history": 0}, "investigation": {"profile": True, "history": 200},
             "evidence": {"profile": True, "history": 200}}


class Saving(BaseModel):
    model_config = ConfigDict(extra="forbid")
    messages: StrictBool = True
    edits: StrictBool = True
    deletions: StrictBool = True
    reactions: StrictBool = True
    membership: StrictBool = True
    media: Literal[MEDIA] = "standard"
    history: Literal[HISTORY] = "none"
    timestamps: StrictBool = False


class Chats(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["selected", "folder", "account"] = "selected"
    chat_ids: list[int] = Field(default_factory=list, max_length=EXCLUDE_LIMIT)
    folder_id: int | None = Field(default=None, ge=0, le=4096)
    types: SourceTypes = Field(default_factory=SourceTypes)
    acknowledged: StrictBool = False


class Answers(BaseModel):
    """What was chosen so far; every answer may still be missing while the person is on the way."""
    model_config = ConfigDict(extra="forbid")
    goal: Literal[GOALS] | None = None
    purpose: Literal[PURPOSES] | None = None
    account_kind: Literal["dedicated", "main"] | None = None
    chats: Chats | None = None
    saving: Saving | None = None
    place: Literal[levels.PLACES] | None = None


class Progress(BaseModel):
    model_config = ConfigDict(extra="forbid")
    step: Literal[STEPS] = "goal"
    answers: Answers = Field(default_factory=Answers)


class Incomplete(ValueError):
    """An answer the plan needs is missing; step names the page that asks for it."""
    def __init__(self, step, message):
        super().__init__(message)
        self.step = step


def steps_for(goal):
    return COPY_STEPS if goal == "copy" else STEPS


def kind_of(answers):
    """The goal as the scales and the evidence settings know it (levels.GOALS)."""
    if answers.goal == "evidence":
        return "evidence"
    if answers.goal == "watch":
        return answers.purpose or "investigation"
    return None


def presets():
    """What each goal suggests on the chats and saving pages; the person may change every value."""
    def saving(**values):
        return Saving(**values).model_dump()
    return {
        "personal": {"chats": "selected", "saving": saving(reactions=False, membership=False, media="small")},
        "investigation": {"chats": "account", "saving": saving(media="standard", history="recent", timestamps=True)},
        "evidence": {"chats": "selected", "saving": saving(media="standard", history="recent", timestamps=True)},
    }


def load(store):
    """The saved progress with its bookkeeping (when it finished or was skipped, what was applied)."""
    saved = store.get_setting("setup_wizard", None) or {}
    # Answers a later version no longer asks are left out rather than discarding the rest.
    answers = {key: value for key, value in (saved.get("answers") or {}).items() if key in Answers.model_fields}
    try:
        progress = Progress(step=saved.get("step", "goal"), answers=answers)
    except ValueError:
        progress = Progress()
    return {**progress.model_dump(), "updated_at": saved.get("updated_at"),
            "finished_at": saved.get("finished_at"), "skipped_at": saved.get("skipped_at"),
            "applied": saved.get("applied")}


def flags(store):
    """For the panel's status: whether the wizard was completed or skipped, and where it stopped."""
    saved = store.get_setting("setup_wizard", None) or {}
    return {"finished": bool(saved.get("finished_at")), "skipped": bool(saved.get("skipped_at")),
            "step": saved.get("step") if saved.get("step") in STEPS else "goal"}


def save(store, now, **changes):
    saved = {**(store.get_setting("setup_wizard", None) or {}), **changes, "updated_at": now}
    store.set_setting("setup_wizard", saved)
    return load(store)


def media_capture(choice, capture):
    """The attachment policy for an answer, keeping the parts the wizard does not ask about."""
    if choice == "none":
        return {**capture, "download_media": False}
    sizes = {"small": {kind: min(SMALL_MEDIA_MB, MEDIA_DEFAULT_MB[kind]) for kind in MEDIA_TYPES},
             "standard": MEDIA_DEFAULT_MB, "all": levels.LARGE_MEDIA_MB}[choice]
    return {"download_media": True, "record_disabled_media": capture["record_disabled_media"],
            "max_media_mb": max(sizes.values()),
            "types": {kind: {"enabled": True, "max_mb": sizes[kind]} for kind in MEDIA_TYPES}}


def media_choice(capture):
    """The answer that matches the current attachment policy, for a wizard opened again."""
    if not capture["download_media"]:
        return "none"
    rules = capture["types"]
    for choice in ("all", "standard", "small"):
        wanted = media_capture(choice, capture)["types"]
        if all(rules[kind]["enabled"] and rules[kind]["max_mb"] == wanted[kind]["max_mb"] for kind in MEDIA_TYPES):
            return choice
    return "standard"


def size_for(chats, dialog_limit):
    current = levels.size_choice(dialog_limit)
    if chats.mode == "account":
        return "large"
    if chats.mode == "folder" and current == "small":
        return "medium"
    return current


def plan(answers, current):
    """What applying the answers sets: scope, chosen chats, live events, attachments and the goal.

    current holds scope, monitoring, capture, evidence, parameters (tuning values) and targets.
    Raises Incomplete with the step to return to when an answer is missing.
    """
    goal = kind_of(answers)
    if goal is None:
        raise Incomplete("goal", "Choose what you need first.")
    chats, saving = answers.chats, answers.saving
    if chats is None:
        raise Incomplete("chats", "Choose the chats to record.")
    if chats.mode == "selected" and not chats.chat_ids:
        raise Incomplete("chats", "Choose at least one chat to record.")
    if chats.mode == "folder" and chats.folder_id is None:
        raise Incomplete("chats", "Choose a Telegram folder. Load chats first if the list is empty.")
    if saving is None:
        raise Incomplete("saving", "Choose what to save.")
    if answers.place is None:
        raise Incomplete("place", "Choose where TgWitness runs.")
    # Kinds of chats and what a new chat brings matter only where chats are added by the scope.
    scope = {**current["scope"], "mode": chats.mode,
             "folder_id": chats.folder_id if chats.mode == "folder" else None}
    if chats.mode != "selected":
        scope.update(types=chats.types.model_dump(), new_chats=NEW_CHATS[goal])
    wide = chats.mode != "selected" and (chats.mode != current["scope"]["mode"]
                                         or scope["folder_id"] != current["scope"]["folder_id"])
    if wide and not chats.acknowledged:
        raise Incomplete("chats", "Confirm that this is a dedicated account before recording a folder or the whole account.")
    monitoring = {name: getattr(saving, name) for name in ("messages", "edits", "deletions", "reactions", "membership")}
    capture = media_capture(saving.media, current["capture"])
    recommended = levels.RECOMMENDED[goal]["apply"]
    setup = levels.Setup(goal=goal, size=size_for(chats, current["parameters"]["dialog_limit"]),
                         files={"none": "text", "small": "media", "standard": "media", "all": "all"}[saving.media],
                         place=answers.place, timestamps=saving.timestamps,
                         drand=saving.timestamps and "drand" in recommended,
                         devices=saving.timestamps and "devices" in recommended)
    planned = levels.plan(setup, current["evidence"], capture, current["parameters"])
    enabled = {t["chat_id"] for t in current["targets"] if t["enabled"]}
    chosen = list(dict.fromkeys(chats.chat_ids)) if chats.mode == "selected" else []
    return {"goal": goal, "scope": scope, "acknowledged": wide, "monitoring": monitoring, "capture": capture,
            "setup": setup, "evidence": planned["evidence"], "parameters": planned["parameters"],
            "enable": [c for c in chosen if c not in enabled],
            "pause": sorted(enabled - set(chosen)) if chats.mode == "selected" else []}


def summary(current):
    """The values the wizard sets, as they are now; compared with a plan and with what was applied."""
    return {"scope": {key: current["scope"][key] for key in ("mode", "folder_id", "types", "new_chats")},
            "monitoring": current["monitoring"], "media": media_choice(current["capture"]),
            "timestamps": bool(current["evidence"]["enabled"])}


def drift(applied, current):
    """Settings changed by hand after the wizard applied them: the parts that no longer match."""
    if not applied:
        return []
    now = summary(current)
    return [key for key in ("scope", "monitoring", "media", "timestamps") if applied.get(key) != now[key]]
