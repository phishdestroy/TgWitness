import time

MEANING = ("Text (history, export) uses the account's main Telethon sender. "
           "Media uses the per-DC pool from multi_connection.py. "
           "A FloodWait on one lane does not block the other unless Telegram issues a global wait.")


class LaneRouter:
    def __init__(self, client):
        self.client = client
        self._text_blocked_until = 0.0
        self._media_blocked_until = 0.0

    def text_sender(self):
        return self.client._sender

    def media_sender(self, dc_id):
        pool = getattr(self.client, "multi_connection_pool", None)
        if pool is None:
            return self.client._sender
        return pool.get(dc_id)

    def set_text_backoff(self, seconds, *, clock=time.monotonic):
        self._text_blocked_until = clock() + seconds

    def set_media_backoff(self, seconds, *, clock=time.monotonic):
        self._media_blocked_until = clock() + seconds

    def text_ready(self, *, clock=time.monotonic):
        return clock() >= self._text_blocked_until

    def media_ready(self, *, clock=time.monotonic):
        return clock() >= self._media_blocked_until

    def text_backoff_remaining(self, *, clock=time.monotonic):
        return max(0.0, self._text_blocked_until - clock())

    def media_backoff_remaining(self, *, clock=time.monotonic):
        return max(0.0, self._media_blocked_until - clock())

    def public(self, *, clock=time.monotonic):
        now = clock()
        pool = getattr(self.client, "multi_connection_pool", None)
        return {
            "text": {"blocked_seconds": max(0.0, round(self._text_blocked_until - now, 1))},
            "media": {
                "blocked_seconds": max(0.0, round(self._media_blocked_until - now, 1)),
                "pool": pool.public() if pool is not None else None,
            },
        }
