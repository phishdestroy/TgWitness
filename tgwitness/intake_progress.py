class IntakeProgress:
    def __init__(self, store):
        self.store = store
        with store.transaction():
            store.db.execute("CREATE TABLE IF NOT EXISTS chat_intake_progress ("
                "chat_id INTEGER NOT NULL, baseline INTEGER NOT NULL, "
                "history_done INTEGER NOT NULL DEFAULT 0, profile_done INTEGER NOT NULL DEFAULT 0, "
                "attempts INTEGER NOT NULL DEFAULT 0, retry_at REAL NOT NULL DEFAULT 0, "
                "error_type TEXT, error_seq INTEGER, PRIMARY KEY(chat_id,baseline))")

    def get(self, chat_id, baseline):
        with self.store.reading() as db:
            row = db.execute("SELECT * FROM chat_intake_progress WHERE chat_id=? AND baseline=?",
                             (chat_id, int(baseline))).fetchone()
        return dict(row) if row else {}

    def done(self, chat_id, baseline, stage):
        if stage not in ("history", "profile"):
            raise ValueError("Unknown intake stage")
        field = stage + "_done"
        with self.store.transaction():
            self.store.db.execute("INSERT INTO chat_intake_progress(chat_id,baseline," + field + ") VALUES (?,?,1) "
                "ON CONFLICT(chat_id,baseline) DO UPDATE SET " + field + "=1", (chat_id, int(baseline)))

    def defer(self, chat_id, baseline, attempts, retry_at, error_type, error_seq):
        with self.store.transaction():
            self.store.db.execute("INSERT INTO chat_intake_progress(chat_id,baseline,attempts,retry_at,error_type,error_seq) "
                "VALUES (?,?,?,?,?,?) ON CONFLICT(chat_id,baseline) DO UPDATE SET "
                "attempts=excluded.attempts,retry_at=excluded.retry_at,error_type=excluded.error_type,error_seq=excluded.error_seq",
                (chat_id, int(baseline), attempts, retry_at, error_type, error_seq))

    def retries(self):
        with self.store.reading() as db:
            return [dict(row) for row in db.execute("SELECT chat_id,baseline,attempts,retry_at,error_type,error_seq "
                "FROM chat_intake_progress WHERE error_type IS NOT NULL")]

    def clear(self, chat_id, baseline):
        key = "baseline_pending" if baseline else "new_chat_intake_pending"
        with self.store.transaction():
            self.store.set_setting(key, [c for c in self.store.get_setting(key, []) if c != chat_id])
            self.store.db.execute("DELETE FROM chat_intake_progress WHERE chat_id=? AND baseline=?",
                                  (chat_id, int(baseline)))
