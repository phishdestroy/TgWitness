HANDOVER_SECONDS = 15
REBALANCE_SECONDS = 10
SLOWER_BY = 1.2
YIELD_PAUSE = 2
METHOD = "messages.getHistory"
MEANING = ("A range that an account cannot continue soon is handed to another account at its last signed page. "
           "Pages already signed stay with the account that read them; the next page names the account it took "
           "the range from.")


class Handover(Exception):
    def __init__(self, seconds=0, reason="flood_wait"):
        super().__init__(reason)
        self.seconds, self.reason = seconds, reason


def gap_of(collector, method=METHOD):
    pacer = getattr(getattr(collector, "client", None), "bulk_pacer", None)
    try:
        return pacer.recommended_gap_ms(method) if pacer is not None else None
    except Exception:
        return None


def slow_holders(gaps, holders, idle, slower_by=SLOWER_BY):
    known = [gaps[worker] for worker in idle if gaps.get(worker)]
    if not known:
        return set()
    best = min(known)
    return {worker for worker in holders if worker not in idle and gaps.get(worker) and gaps[worker] >= best * slower_by}
