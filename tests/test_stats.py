"""Tests for persistent token stats."""

import json
import pytest
from lomsh import stats as stats_module


@pytest.fixture(autouse=True)
def tmp_stats_file(tmp_path, monkeypatch):
    """Redirect STATS_FILE to a temp path so tests don't touch ~/.lomsh_stats.json."""
    fake = str(tmp_path / "stats.json")
    monkeypatch.setattr(stats_module, "STATS_FILE", fake)
    return fake


def test_load_alltime_missing_file():
    assert stats_module.load_alltime() == (0, 0)


def test_save_then_load():
    stats_module.save_alltime(100, 50)
    assert stats_module.load_alltime() == (100, 50)


def test_save_accumulates():
    stats_module.save_alltime(100, 50)
    stats_module.save_alltime(200, 75)
    assert stats_module.load_alltime() == (300, 125)


def test_load_handles_corrupt_file(tmp_path, monkeypatch):
    fake = str(tmp_path / "corrupt.json")
    monkeypatch.setattr(stats_module, "STATS_FILE", fake)
    with open(fake, "w") as f:
        f.write("not json{{{")
    assert stats_module.load_alltime() == (0, 0)


def test_save_zero_sessions():
    stats_module.save_alltime(0, 0)
    assert stats_module.load_alltime() == (0, 0)
