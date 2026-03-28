"""Persistent token stats — accumulates across sessions in ~/.lomsh_stats.json."""

import json
import os

STATS_FILE = os.path.expanduser("~/.lomsh_stats.json")


def load_alltime() -> tuple[int, int]:
    """Return (total_in, total_out) from the stats file. Returns (0, 0) if missing."""
    try:
        with open(STATS_FILE) as f:
            d = json.load(f)
            return d.get("in", 0), d.get("out", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0, 0


def save_alltime(session_in: int, session_out: int) -> None:
    """Add this session's tokens to the running all-time totals."""
    prev_in, prev_out = load_alltime()
    with open(STATS_FILE, "w") as f:
        json.dump({"in": prev_in + session_in, "out": prev_out + session_out}, f)
