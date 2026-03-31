"""Tests for CLI-level behaviour — tab completion and readline history."""

import os
import glob
import pytest
from lomsh.shell import Session


# ── path completer ────────────────────────────────────────────────────────────

import re as _re


# ── prompt width ──────────────────────────────────────────────────────────────

def test_prompt_ansi_wrapped_for_readline(tmp_path):
    """Every ANSI escape in the prompt must be wrapped in \\001/\\002."""
    from lomsh.shell import Session
    from lomsh.cli import make_prompt

    s = Session()
    s.cwd = str(tmp_path)
    prompt = make_prompt(s)

    # Find all ANSI escapes — each must be preceded by \001 and followed by \002
    escapes = list(_re.finditer(r"\033\[[^m]*m", prompt))
    assert escapes, "prompt should contain at least one ANSI escape"
    for m in escapes:
        start = m.start()
        end   = m.end()
        assert prompt[start - 1] == "\001", f"escape at {start} not preceded by \\001"
        assert prompt[end]       == "\002", f"escape at {end} not followed by \\002"


def test_prompt_contains_no_bare_escapes(tmp_path):
    """No ANSI escape should appear outside \\001/\\002 markers."""
    from lomsh.shell import Session
    from lomsh.cli import make_prompt

    s = Session()
    s.cwd = str(tmp_path)
    prompt = make_prompt(s)

    # Strip wrapped sequences — nothing should remain
    stripped = _re.sub(r"\001\033\[[^m]*m\002", "", prompt)
    assert "\033" not in stripped


def _make_completer(session):
    """Recreate the _path_completer closure from cli.py for testing."""
    def _path_completer(text, state):
        if os.path.isabs(text) or text.startswith("~"):
            pattern = os.path.expanduser(text) + "*"
            base = None
        else:
            pattern = os.path.join(session.cwd, text) + "*"
            base = session.cwd
        matches = glob.glob(pattern)
        results = []
        for m in matches:
            rel = os.path.relpath(m, base) if base else m
            results.append(rel + "/" if os.path.isdir(m) else rel)
        try:
            return results[state]
        except IndexError:
            return None
    return _path_completer


def test_completer_finds_subdir(tmp_path):
    """Completer should find a subdirectory relative to session.cwd."""
    subdir = tmp_path / "myproject"
    subdir.mkdir()

    s = Session()
    s.cwd = str(tmp_path)
    completer = _make_completer(s)

    result = completer("myp", 0)
    assert result == "myproject/"


def test_completer_uses_session_cwd_not_process_cwd(tmp_path):
    """Completer must use session.cwd even when the process cwd is different."""
    subdir = tmp_path / "targetdir"
    subdir.mkdir()

    s = Session()
    s.cwd = str(tmp_path)   # session is in tmp_path
    # process cwd is wherever pytest is running — definitely not tmp_path
    completer = _make_completer(s)

    result = completer("target", 0)
    assert result == "targetdir/"


def test_completer_returns_none_when_no_match(tmp_path):
    s = Session()
    s.cwd = str(tmp_path)
    completer = _make_completer(s)

    assert completer("zzznomatch", 0) is None


def test_completer_appends_slash_for_dirs(tmp_path):
    (tmp_path / "adir").mkdir()
    s = Session()
    s.cwd = str(tmp_path)
    completer = _make_completer(s)
    result = completer("adir", 0)
    assert result.endswith("/")


def test_completer_no_slash_for_files(tmp_path):
    (tmp_path / "afile.txt").write_text("x")
    s = Session()
    s.cwd = str(tmp_path)
    completer = _make_completer(s)
    result = completer("afile", 0)
    assert result == "afile.txt"
    assert not result.endswith("/")


def test_completer_absolute_path(tmp_path):
    (tmp_path / "thing").mkdir()
    s = Session()
    s.cwd = "/some/other/dir"   # session.cwd is irrelevant for absolute paths
    completer = _make_completer(s)
    result = completer(str(tmp_path) + "/thi", 0)
    assert result is not None
    assert "thing" in result


# ── readline history ──────────────────────────────────────────────────────────

def test_history_file_written_on_exit(tmp_path):
    """write_history_file should create a file containing prior commands."""
    import readline
    history_file = str(tmp_path / "test_history")

    readline.add_history("gitlog")   # no spaces — libedit encodes spaces as \040
    readline.add_history("pwd")
    readline.write_history_file(history_file)

    assert os.path.exists(history_file)
    # Read back via readline to avoid format assumptions (libedit vs GNU)
    readline.clear_history()
    readline.read_history_file(history_file)
    history = [readline.get_history_item(i) for i in range(1, readline.get_current_history_length() + 1)]
    assert "gitlog" in history
    assert "pwd" in history


def test_history_file_loaded_on_startup(tmp_path):
    """write then read round-trip should restore commands."""
    import readline
    history_file = str(tmp_path / "test_history")

    readline.add_history("lsla")
    readline.add_history("pwd")
    readline.write_history_file(history_file)

    readline.clear_history()
    readline.read_history_file(history_file)

    history = [readline.get_history_item(i) for i in range(1, readline.get_current_history_length() + 1)]
    assert "lsla" in history
    assert "pwd" in history


def test_missing_history_file_does_not_crash(tmp_path):
    """Loading a non-existent history file should be handled gracefully."""
    import readline
    try:
        readline.read_history_file(str(tmp_path / "nonexistent_history"))
    except FileNotFoundError:
        pass  # expected — caller catches this
    # no exception propagated = pass
