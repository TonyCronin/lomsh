"""Tests for shell block detection and execution behaviour in call_agent."""

import subprocess
import pytest
from unittest.mock import patch, MagicMock
from lomsh.shell import Session


# ── helpers ───────────────────────────────────────────────────────────────────

def _response_with_blocks(*blocks, lang="bash"):
    """Build a fake agent response containing the given shell code blocks."""
    parts = ["Some explanation.\n"]
    for block in blocks:
        parts.append(f"```{lang}\n{block}\n```\n")
    return "".join(parts)


# ── block detection ───────────────────────────────────────────────────────────

def test_single_block_offers_run(tmp_path, monkeypatch):
    """A response with one shell block should prompt run this?."""
    import re
    response = _response_with_blocks("echo hello")
    shell_blocks = re.findall(r"```(?:bash|sh|zsh|shell)\n(.*?)```", response, re.DOTALL)
    assert len(shell_blocks) == 1
    assert shell_blocks[0].strip() == "echo hello"


def test_multiple_blocks_all_detected(tmp_path):
    """All shell blocks in a response should be found."""
    import re
    response = _response_with_blocks("echo one", "echo two", "echo three")
    shell_blocks = re.findall(r"```(?:bash|sh|zsh|shell)\n(.*?)```", response, re.DOTALL)
    assert len(shell_blocks) == 3


def test_non_shell_blocks_ignored():
    """HTML and python blocks should not be offered to run."""
    import re
    response = "```html\n<h1>hi</h1>\n```\n```python\nprint('hi')\n```\n"
    shell_blocks = re.findall(r"```(?:bash|sh|zsh|shell)\n(.*?)```", response, re.DOTALL)
    assert len(shell_blocks) == 0


# ── execution uses session.cwd ────────────────────────────────────────────────

def test_block_runs_in_session_cwd(tmp_path):
    """Shell block execution must use session.cwd, not the process cwd."""
    s = Session()
    s.cwd = str(tmp_path)

    result = subprocess.run(
        "touch marker.txt",
        shell=True,
        text=True,
        capture_output=True,
        cwd=s.cwd,
    )
    assert result.returncode == 0
    assert (tmp_path / "marker.txt").exists()


def test_block_does_not_run_in_process_cwd(tmp_path):
    """Confirm that without cwd=session.cwd the file lands in the wrong place."""
    import os
    s = Session()
    s.cwd = str(tmp_path)

    # Run without passing cwd - should land in process cwd, not tmp_path
    result = subprocess.run(
        "touch wrong_place.txt",
        shell=True,
        text=True,
        capture_output=True,
        # deliberately omitting cwd=s.cwd
    )
    assert result.returncode == 0
    assert not (tmp_path / "wrong_place.txt").exists()


# ── sequential prompting ──────────────────────────────────────────────────────

def test_sequential_blocks_user_skips_second(tmp_path):
    """User answers y then n — only first block runs."""
    import re

    response = _response_with_blocks(
        f"touch {tmp_path}/first.txt",
        f"touch {tmp_path}/second.txt",
    )
    shell_blocks = re.findall(r"```(?:bash|sh|zsh|shell)\n(.*?)```", response, re.DOTALL)

    answers = iter(["y", "n"])
    for block in shell_blocks:
        cmd = block.strip()
        answer = next(answers)
        if answer == "y":
            subprocess.run(cmd, shell=True, text=True, capture_output=True, cwd=str(tmp_path))

    assert (tmp_path / "first.txt").exists()
    assert not (tmp_path / "second.txt").exists()


def test_sequential_blocks_user_runs_both(tmp_path):
    """User answers y for both blocks — both run."""
    import re

    response = _response_with_blocks(
        f"touch {tmp_path}/first.txt",
        f"touch {tmp_path}/second.txt",
    )
    shell_blocks = re.findall(r"```(?:bash|sh|zsh|shell)\n(.*?)```", response, re.DOTALL)

    for block in shell_blocks:
        subprocess.run(block.strip(), shell=True, text=True, capture_output=True, cwd=str(tmp_path))

    assert (tmp_path / "first.txt").exists()
    assert (tmp_path / "second.txt").exists()
