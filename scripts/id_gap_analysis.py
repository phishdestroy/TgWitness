"""Standalone ID gap analysis for a TgWitness data directory.

Usage: python scripts/id_gap_analysis.py <data_dir> [--chat CHAT_ID] [--min-gap N] [--top N] [--json]
"""
import argparse
import json
import sqlite3
import sys
from pathlib import Path


CHANNEL_IDS_BELOW = -1000000000000
MESSAGE_KINDS = ("message.new", "message.snapshot", "message.edited",
                 "message.recovered", "message.deleted", "message.missing_on_recheck")


def gap_size_label(n):
    if n == 0:
        return "none"
    if n <= 5:
        return "small"
    if n <= 50:
        return "medium"
    return "large"


def analyze_chat(rows):
    times = {}
    for row in rows:
        msg_id = row["message_id"]
        if isinstance(msg_id, int) and msg_id > 0:
            times[msg_id] = row["observed_at"]
    if len(times) < 2:
        return None
    ordered = sorted(times)
    holes = [(lo + 1, hi - 1) for lo, hi in zip(ordered, ordered[1:]) if hi - lo > 1]
    missing = sum(hi - lo + 1 for lo, hi in holes)
    return {
        "observed": len(ordered),
        "span": ordered[-1] - ordered[0] + 1,
        "missing": missing,
        "gap_ranges": len(holes),
        "largest_gap": max((hi - lo + 1 for lo, hi in holes), default=0),
        "size_label": gap_size_label(missing),
        "gaps": [{"low": lo, "high": hi, "missing": hi - lo + 1} for lo, hi in holes],
    }


def run(data_dir, chat_id=None, min_gap=1, top=20, as_json=False):
    db_path = Path(data_dir) / "journal.db"
    if not db_path.exists():
        sys.exit("journal.db not found in " + str(data_dir))
    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    placeholders = ",".join("?" * len(MESSAGE_KINDS))
    if chat_id is not None:
        rows = con.execute(
            "SELECT chat_id, message_id, observed_at FROM events "
            "WHERE kind IN (" + placeholders + ") AND chat_id=? AND message_id IS NOT NULL",
            MESSAGE_KINDS + (chat_id,)).fetchall()
        chats = {chat_id: rows}
    else:
        rows = con.execute(
            "SELECT chat_id, message_id, observed_at FROM events "
            "WHERE kind IN (" + placeholders + ") AND message_id IS NOT NULL "
            "AND chat_id < ?",
            MESSAGE_KINDS + (CHANNEL_IDS_BELOW,)).fetchall()
        chats = {}
        for row in rows:
            chats.setdefault(row["chat_id"], []).append(row)
    con.close()

    results = []
    for cid, chat_rows in chats.items():
        summary = analyze_chat(chat_rows)
        if summary and summary["missing"] >= min_gap:
            results.append({"chat_id": cid, **summary})

    results.sort(key=lambda r: -r["missing"])
    results = results[:top]

    if as_json:
        print(json.dumps(results, indent=2))
        return

    for r in results:
        print(f"chat {r['chat_id']}: {r['missing']} missing / {r['gap_ranges']} ranges "
              f"({r['size_label']}) observed={r['observed']} span={r['span']}")
        for g in r["gaps"][:5]:
            print(f"  [{g['low']}–{g['high']}] {g['missing']} missing")
        if len(r["gaps"]) > 5:
            print(f"  ... and {len(r['gaps']) - 5} more ranges")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_dir")
    parser.add_argument("--chat", type=int, default=None)
    parser.add_argument("--min-gap", type=int, default=1)
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    run(args.data_dir, chat_id=args.chat, min_gap=args.min_gap, top=args.top, as_json=args.json)
