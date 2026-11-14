import time
from datetime import datetime

from . import message_content
from .journal_index import attachment_key, raw_attachment
from .scope import recheck_settings
from .store import utcnow

CHANNEL_FLOOR = -1000000000000
SESSIONS_MAX_AGE = 600
RIGHTS_MAX_AGE = 24 * 3600
CLEAR_MIN_IDS = 10
ATTRIBUTIONS = ("own_action", "peer_or_admin", "unknown_other_session_present")
ATTRIBUTION_MEANING = (
    "Who could have deleted the message, from the facts this collector held when the notice arrived; Telegram's "
    "notice does not name who deleted. peer_or_admin: no session of this account could have deleted it, so the other "
    "side, a chat administrator or Telegram removed it. unknown_other_session_present: this account itself, from "
    "another session or device, may have deleted it. own_action: deleted from this workspace, which has no function "
    "that deletes messages. A notice recovered through getDifference arrived after the deletion, at an unknown "
    "later time, so the session check made when it arrived is not used for it.")
CLEAR_MEANING = (
    "Suspected: one deletion notice for a private chat removed at least {n} saved messages, including messages this "
    "account sent, and no saved message between the first and the last of them is left. Clearing the history for "
    "both sides produces such a notice; so does a selection of messages deleted for both sides, or a clear made for "
    "this account only from another of its sessions. The notice itself does not say which.")
SHORTENED_MEANING = (
    "Deletion notices arrived in this priority chat for messages whose content this journal never held. Its recheck "
    "interval is shortened so that messages arriving in it are read before they can be deleted; the interval returns "
    "to the configured value once no such notice arrives during one shortened interval.")
RESTORED_MEANING = ("No deletion notice for a never-saved message arrived in this chat during one shortened recheck "
                    "interval. The configured interval applies again.")
TEXTS = {
    "account_cannot_delete_here": "Not deleted by this account: it had no right to delete this message in this chat. "
                                  "Its author, a chat administrator or Telegram removed it.",
    "no_other_session": "Not deleted by this account: it had no other signed-in session at the session check {seconds} s "
                        "earlier, and this workspace does not delete messages. The other side, a chat administrator "
                        "or Telegram removed it.",
    "this_account_may_have_deleted": "Who deleted it is not known: this account itself, from another session or "
                                     "device, could also have deleted it.",
}
UNDETERMINED = "Who deleted it was not determined."
CLEAR_TEXT = ("Suspected clear of the chat history: one deletion notice removed {n} saved messages, numbers {first} to "
              "{last}, {ours} of them sent by this account, and left no saved message in between.")
LINKED = "The chat's admin log names user {id} as the account that deleted it."
LINKED_SELF = "The chat's admin log names this account as the one that deleted it."


def age(value, now=None):
    try:
        return max(0, round((now or time.time()) - datetime.fromisoformat(value).timestamp()))
    except (TypeError, ValueError):
        return None


def account_id(store):
    return (store.get_setting("account", {}) or {}).get("id")


def rights_fact(store, chat_id):
    entry = (store.get_setting("own_rights", {}) or {}).get(str(chat_id))
    if not isinstance(entry, dict):
        return None
    return {**entry, "age_seconds": age(entry.get("checked_at"))}


def sessions_fact(store):
    check = store.get_setting("sessions_checked", None)
    if not isinstance(check, dict):
        return None
    return {"checked_at": check.get("at"), "age_seconds": age(check.get("at")),
            "other_sessions": check.get("others"), "this_session_listed": check.get("current")}


def attribution_context(store, chat_id, recovered=False):
    return {"chat_type": chat_type(store, chat_id, account_id(store)),
            "rights": rights_fact(store, chat_id) if chat_id < CHANNEL_FLOOR else None,
            "sessions_check": sessions_fact(store), "workspace_deletes_messages": False,
            **({"recovered_through_difference": True, "sessions_check_used": False} if recovered else {}),
            "limits": {"sessions_max_age_seconds": SESSIONS_MAX_AGE, "rights_max_age_seconds": RIGHTS_MAX_AGE},
            "meaning": ATTRIBUTION_MEANING}


def chat_type(store, chat_id, me):
    if chat_id == me:
        return "saved_messages"
    if chat_id > 0:
        return "private"
    if chat_id > CHANNEL_FLOOR:
        return "basic_group"
    kind = ((store.get_setting("own_rights", {}) or {}).get(str(chat_id)) or {}).get("chat_type") or next(
        (t["kind"] for t in store.targets() if t["chat_id"] == chat_id), None)
    return kind if kind in ("channel", "supergroup") else "channel_or_supergroup"


def account_can_delete(kind, author, rights):
    if kind in ("private", "basic_group", "saved_messages") or author == "this_account":
        return True
    fresh = (rights is not None and rights.get("role") in ("creator", "admin", "member")
             and rights.get("age_seconds") is not None and rights["age_seconds"] <= RIGHTS_MAX_AGE)
    if not fresh:
        return None
    if rights["role"] == "creator" or rights.get("delete_messages"):
        return True
    if author == "another_account" or kind == "channel" and rights["role"] == "member":
        return False
    return None


def attribution(store, chat_id, content, batched=False, recovered=False):
    context = attribution_context(store, chat_id, recovered)
    kind, rights, sessions = context["chat_type"], context["rights"], context["sessions_check"]
    outgoing = (content or {}).get("outgoing")
    author = "unknown" if outgoing is None else "this_account" if outgoing else "another_account"
    can = account_can_delete(kind, author, rights)
    if can is False:
        value, rule = "peer_or_admin", "account_cannot_delete_here"
    elif (not recovered and kind != "saved_messages" and sessions and sessions["other_sessions"] == 0
          and sessions["this_session_listed"] and sessions["age_seconds"] is not None
          and sessions["age_seconds"] <= SESSIONS_MAX_AGE):
        value, rule = "peer_or_admin", "no_other_session"
    else:
        value, rule = "unknown_other_session_present", "this_account_may_have_deleted"
    facts = {"rule": rule, "message_author": author, "this_account_could_delete": can}
    if batched:
        facts.update(context="deletion.batch", sessions_age_seconds=(sessions or {}).get("age_seconds"))
        if recovered:
            facts["recovered_through_difference"] = True
    else:
        facts.update(context)
    return {"attribution": value, "attribution_facts": facts}


def attribution_text(say, payload, link=None):
    if isinstance(link, dict) and type(link.get("actor_id")) is int:
        return say(LINKED_SELF) if link.get("actor_is_this_account") else say(LINKED, id=link["actor_id"])
    facts = payload.get("attribution_facts") if isinstance(payload.get("attribution_facts"), dict) else {}
    rule = facts.get("rule")
    if payload.get("attribution") not in ATTRIBUTIONS or rule not in TEXTS:
        return say(UNDETERMINED)
    if rule == "no_other_session":
        seconds = (facts.get("sessions_check") or {}).get("age_seconds", facts.get("sessions_age_seconds"))
        return say(TEXTS[rule], seconds=seconds if type(seconds) is int else "?")
    return say(TEXTS[rule])


def clear_text(say, payload):
    return (say(CLEAR_TEXT, n=payload.get("message_ids", "?"), first=payload.get("first_id", "?"),
                last=payload.get("last_id", "?"), ours=payload.get("outgoing", "?"))
            + " " + attribution_text(say, payload))


def previous_version(store, content, payload):
    before, after = content["observable"], message_content.of_payload(payload)
    changed = sorted(key for key in after if before.get(key) != after[key])
    if content.get("edited_at") != payload.get("edited_at"):
        changed.append("edited_at")
    found = {"seq": content["seq"], "hash": content["hash"], "changed": changed}
    if "media" in changed:
        old, new = raw_attachment(before.get("media")), raw_attachment(after.get("media"))
        saved = store.stored_media(attachment_key(old)) if old else None
        found["media"] = {"before": {**old, **({"sha256": saved["sha256"], "media_event": saved["seq"]} if saved else {})}
                          if old else None, "after": new,
                          "same_file": None if not (old and new) else old["kind"] == new["kind"] and old["id"] == new["id"]}
    return found


def clear_suspected(store, chat_id, ids, notice_ids, raw, batch, source=None):
    me = account_id(store)
    if chat_id <= 0 or chat_id == me or len(ids) < CLEAR_MIN_IDS:
        return None
    states = [store.message_state(chat_id, message_id) for message_id in ids]
    ours = sum(1 for state in states if (state["content"] or {}).get("outgoing"))
    if not ours:
        return None
    low, high = min(ids), max(ids)
    with store.lock:
        left = store.db.execute(
            "SELECT 1 FROM message_state_index WHERE chat_id=? AND message_id BETWEEN ? AND ? AND text_seq IS NOT NULL "
            "AND deleted=0 AND missing=0 LIMIT 1", (chat_id, low, high)).fetchone()
    if left:
        return None
    return store.append("history.cleared_by_peer_suspected", {
        "message_ids": len(ids), "first_id": low, "last_id": high, "outgoing": ours, "incoming": len(ids) - ours,
        "content_preserved": sum(1 for state in states if state["content"]),
        "notice_ids": len(notice_ids), "notice_ids_not_in_this_chat_or_unsaved": len(notice_ids) - len(ids),
        "conditions": {"chat": "private", "min_message_ids": CLEAR_MIN_IDS, "includes_outgoing": True,
                       "no_saved_message_left_in_range": True},
        **attribution(store, chat_id, None, recovered=bool(source)), "source": source or "live_update",
        **({"batch": batch} if batch else {"raw": raw}),
        "meaning": CLEAR_MEANING.format(n=CLEAR_MIN_IDS)}, chat_id)


def unobserved(store, chat_id):
    with store.lock:
        row = store.db.execute("SELECT deleted-deleted_saved FROM chat_state_index WHERE chat_id=?", (chat_id,)).fetchone()
    return row[0] if row else 0


def priority_target(store, chat_id):
    return next((t for t in store.targets(True) if t["chat_id"] == chat_id and t["priority"]), None)


def interval_floor(collector):
    return max(1, -(-collector.param("recheck_tick_seconds") // 60))


def unobserved_grew(collector, chat_id, before):
    store = collector.store
    count = unobserved(store, chat_id)
    configured = recheck_settings(store)["recheck_minutes"]
    if count <= before or not configured or not priority_target(store, chat_id):
        return None
    shortened = store.get_setting("recheck_shortened", {}) or {}
    entry = shortened.get(str(chat_id))
    current = min(configured, entry["minutes"]) if entry else configured
    floor = interval_floor(collector)
    minutes = min(current, max(floor, current // 2))
    shortened[str(chat_id)] = {"minutes": minutes, "configured_minutes": configured, "count": count,
                               "since": (entry or {}).get("since") or utcnow(), "grew_at": utcnow()}
    store.set_setting("recheck_shortened", shortened)
    if minutes >= current:
        return None
    return store.append("recheck.interval_shortened", {
        "configured_minutes": configured, "previous_minutes": current, "minutes": minutes, "floor_minutes": floor,
        "never_saved_deletions": {"before": before, "after": count},
        "reason": "deletion notices for messages this journal never held", "meaning": SHORTENED_MEANING}, chat_id)


def review_interval(collector, chat_id):
    store = collector.store
    shortened = store.get_setting("recheck_shortened", {}) or {}
    entry = shortened.get(str(chat_id))
    if not entry:
        return None
    count = unobserved(store, chat_id)
    if count > entry["count"]:
        shortened[str(chat_id)] = {**entry, "count": count, "grew_at": utcnow()}
        store.set_setting("recheck_shortened", shortened)
        return None
    priority = priority_target(store, chat_id)
    if priority and (age(entry["grew_at"]) or 0) < entry["minutes"] * 60:
        return None
    del shortened[str(chat_id)]
    store.set_setting("recheck_shortened", shortened)
    return store.append("recheck.interval_restored", {
        "minutes": recheck_settings(store)["recheck_minutes"], "shortened_minutes": entry["minutes"],
        "shortened_since": entry["since"], "last_growth_at": entry["grew_at"], "never_saved_deletions": count,
        "reason": "no new deletion notice for a never-saved message during one shortened interval" if priority
                  else "the chat is no longer a priority chat",
        "meaning": RESTORED_MEANING}, chat_id)


def shortened_minutes(store, chat_id, minutes):
    entry = (store.get_setting("recheck_shortened", {}) or {}).get(str(chat_id))
    return min(minutes, entry["minutes"]) if entry and minutes else minutes
