from telethon.tl import functions

from .swarm.floodwait_learner import FloodWaitLearner


BULK_READS = (functions.messages.GetHistoryRequest, functions.messages.GetDialogsRequest,
              functions.channels.GetAdminLogRequest, functions.messages.GetMessagesRequest,
              functions.channels.GetMessagesRequest, functions.channels.GetParticipantsRequest,
              functions.messages.GetMessagesViewsRequest, functions.contacts.ResolveUsernameRequest,
              functions.channels.GetFullChannelRequest, functions.messages.GetFullChatRequest,
              # Photos of chats and people look up one person after another; unpaced, they hit FLOOD_WAIT in bursts.
              functions.photos.GetUserPhotosRequest)


def bulk_request(request):
    for _ in range(8):
        if isinstance(request, BULK_READS):
            return True
        request = getattr(request, "query", None)
        if request is None:
            return False
    return False


class AccountPacer(FloodWaitLearner):
    pass
