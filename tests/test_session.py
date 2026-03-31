"""Tests for Session and run_command."""

import os
import pytest
from lomsh.shell import Session, run_command


def test_session_initial_cwd():
    s = Session()
    assert s.cwd == os.getcwd()


def test_add_cmd_appears_in_history():
    s = Session()
    s.add_cmd("ls", "file.txt\n", "", 0)
    assert len(s.history) == 1
    assert s.history[0]["cmd"] == "ls"


def test_add_agent_appears_in_history():
    s = Session()
    s.add_agent("hello", "hi there")
    assert s.history[0]["type"] == "agent"
    assert s.history[0]["user"] == "hello"


def test_build_context_contains_cwd():
    s = Session()
    ctx = s.build_context()
    assert f"cwd: {s.cwd}" in ctx


def test_build_context_contains_cmd():
    s = Session()
    s.add_cmd("echo hi", "hi\n", "", 0)
    ctx = s.build_context()
    assert "$ echo hi" in ctx
    assert "hi" in ctx


def test_build_context_shows_exit_code_on_failure():
    s = Session()
    s.add_cmd("false", "", "", 1)
    ctx = s.build_context()
    assert "[exit 1]" in ctx


def test_build_context_contains_agent_exchange():
    s = Session()
    s.add_agent("why?", "because")
    ctx = s.build_context()
    assert "> why?" in ctx
    assert "[assistant]: because" in ctx


def test_cd_updates_cwd(tmp_path):
    s = Session()
    s.cwd = str(tmp_path)
    stdout, stderr, rc = run_command(f"cd {tmp_path}", s)
    assert rc == 0
    assert s.cwd == str(tmp_path)


def test_cd_bare_goes_home():
    s = Session()
    run_command("cd", s)
    assert s.cwd == os.path.expanduser("~")


def test_cd_missing_dir_returns_error(tmp_path):
    s = Session()
    s.cwd = str(tmp_path)
    _, stderr, rc = run_command("cd /this/does/not/exist", s)
    assert rc == 1
    assert "No such file" in stderr


def test_cd_relative_path(tmp_path):
    subdir = tmp_path / "sub"
    subdir.mkdir()
    s = Session()
    s.cwd = str(tmp_path)
    run_command("cd sub", s)
    assert s.cwd == str(subdir)


def test_run_command_captures_stdout(tmp_path):
    s = Session()
    s.cwd = str(tmp_path)
    stdout, _, rc = run_command("echo hello", s)
    assert "hello" in stdout
    assert rc == 0


def test_run_command_captures_stderr(tmp_path):
    s = Session()
    s.cwd = str(tmp_path)
    _, stderr, rc = run_command("ls /no/such/path", s)
    assert rc != 0


# ── file content via shell lands in model context ─────────────────────────────

def test_cat_output_appears_in_context(tmp_path):
    """cat file.py output should be visible to the model via session context."""
    src = tmp_path / "main.py"
    src.write_text("def hello():\n    return 'world'\n")

    s = Session()
    s.cwd = str(tmp_path)
    stdout, _, rc = run_command(f"cat {src}", s)
    assert rc == 0
    s.add_cmd(f"cat {src}", stdout, "", rc)

    ctx = s.build_context()
    assert "def hello():" in ctx
    assert "return 'world'" in ctx


def test_multiple_files_all_in_context(tmp_path):
    """cat of multiple files should put all content in context."""
    (tmp_path / "a.py").write_text("class A: pass\n")
    (tmp_path / "b.py").write_text("class B: pass\n")

    s = Session()
    s.cwd = str(tmp_path)
    stdout, _, rc = run_command(f"cat {tmp_path}/a.py {tmp_path}/b.py", s)
    assert rc == 0
    s.add_cmd("cat a.py b.py", stdout, "", rc)

    ctx = s.build_context()
    assert "class A" in ctx
    assert "class B" in ctx


def test_find_xargs_cat_in_context(tmp_path):
    """find | xargs cat output should land in context for whole-folder reads."""
    src = tmp_path / "app.py"
    src.write_text("# entry point\nimport sys\n")

    s = Session()
    s.cwd = str(tmp_path)
    stdout, _, rc = run_command(f"find {tmp_path} -name '*.py' | xargs cat", s)
    assert rc == 0
    s.add_cmd("find . -name '*.py' | xargs cat", stdout, "", rc)

    ctx = s.build_context()
    assert "entry point" in ctx
    assert "import sys" in ctx
