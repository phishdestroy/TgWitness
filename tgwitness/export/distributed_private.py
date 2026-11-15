import logging

from telethon.tl import functions, types

MEANING = ("Extends distributed chat export to private groups and supergroups. Only accounts that are "
           "confirmed members of the peer receive a split range. Membership is verified via GetParticipants "
           "before assigning any work.")
MEMBERS_LIMIT = 200
log = logging.getLogger(__name__)


async def member_account_ids(client, peer):
    try:
        result = await client(functions.channels.GetParticipantsRequest(
            peer, filter=types.ChannelParticipantsSearch(""),
            offset=0, limit=MEMBERS_LIMIT, hash=0))
        participants = getattr(result, "participants", [])
        return {getattr(p, "user_id", None) for p in participants if getattr(p, "user_id", None)}
    except Exception as exc:
        log.debug("GetParticipants error: %s", exc)
        return set()


async def filter_member_accounts(profiles_with_clients, peer):
    eligible = []
    for profile_id, client, account_id in profiles_with_clients:
        try:
            me = await client.get_me()
            if me is None:
                continue
            my_id = getattr(me, "id", None)
            members = await member_account_ids(client, peer)
            if my_id in members:
                eligible.append((profile_id, client, account_id))
        except Exception as exc:
            log.debug("Member check for profile %s failed: %s", profile_id, exc)
    return eligible


def split_range(start_id, end_id, num_workers):
    if num_workers <= 1:
        return [(start_id, end_id)]
    step = max(1, (end_id - start_id) // num_workers)
    ranges = []
    current = start_id
    for i in range(num_workers):
        next_start = current + step if i < num_workers - 1 else end_id
        ranges.append((current, next_start))
        current = next_start
    return ranges


class DistributedPrivateExport:
    def __init__(self, profiles_registry, *, chat_id, chosen_profiles):
        self.profiles_registry = profiles_registry
        self.chat_id = chat_id
        self.chosen_profiles = list(chosen_profiles)
        self._eligible = None
        self._ranges = []

    async def prepare(self, lead_client, peer):
        profiles_with_clients = []
        for profile_id in self.chosen_profiles:
            try:
                app = self.profiles_registry.app_for(profile_id)
                client = app.state.collector.client
                account_id = (app.state.store.get_setting("account", {}) or {}).get("id")
                profiles_with_clients.append((profile_id, client, account_id))
            except Exception as exc:
                log.debug("Profile %s unavailable: %s", profile_id, exc)
        self._eligible = await filter_member_accounts(profiles_with_clients, peer)
        log.info("DistributedPrivateExport: %s/%s accounts are members",
                 len(self._eligible), len(profiles_with_clients))
        return self._eligible

    def assign_ranges(self, start_id, end_id):
        if not self._eligible:
            raise ValueError("No member accounts available for private distributed export.")
        self._ranges = split_range(start_id, end_id, len(self._eligible))
        return [
            {"profile_id": profile_id, "account_id": account_id,
             "range": {"from_id": r[0], "to_id": r[1]}}
            for (profile_id, _, account_id), r in zip(self._eligible, self._ranges)
        ]

    def public(self):
        return {
            "chat_id": self.chat_id,
            "eligible_accounts": len(self._eligible) if self._eligible is not None else None,
            "ranges": len(self._ranges),
        }
