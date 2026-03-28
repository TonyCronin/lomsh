"""Session state and shell command execution."""

import os
import sys
import subprocess
from collections import deque

SCROLLBACK = 50


class Session:
    """All state for a single lomsh session."""

    def __init__(self):
        self.cwd       = os.getcwd()
        self.env       = os.environ.copy()
        self.history   = deque(maxlen=SCROLLBACK)
        self.total_in  = 0
        self.total_out = 0

    def add_cmd(self, cmd: str, stdout: str, stderr: str, rc: int) -> None:
        self.history.append({"type": "cmd", "cmd": cmd,
                             "stdout": stdout, "stderr": stderr, "rc": rc})

    def add_agent(self, user_msg: str, response: str) -> None:
        self.history.append({"type": "agent", "user": user_msg, "response": response})

    def build_context(self) -> str:
        """Render the full session as a string for the model's system prompt."""
        lines = [
            f"cwd: {self.cwd}",
            f"os: {sys.platform}",
            "",
            "--- session history (oldest first) ---",
        ]
        for entry in self.history:
            if entry["type"] == "cmd":
                lines.append(f"$ {entry['cmd']}")
                if entry["stdout"].strip():
                    lines.append(entry["stdout"].rstrip())
                if entry["stderr"].strip():
                    lines.append(entry["stderr"].rstrip())
                if entry["rc"] != 0:
                    lines.append(f"[exit {entry['rc']}]")
            else:
                lines.append(f"> {entry['user']}")
                lines.append(f"[assistant]: {entry['response']}")
        lines.append("--- end of session history ---")
        return "\n".join(lines)


def run_command(cmd_str: str, session: Session) -> tuple[str, str, int]:
    """
    Execute a shell command in the session's cwd.
    Intercepts `cd` to keep cwd tracked in Python.
    Returns (stdout, stderr, returncode).
    """
    stripped = cmd_str.strip()

    if stripped == "cd" or stripped.startswith("cd "):
        parts  = stripped.split(None, 1)
        target = parts[1] if len(parts) > 1 else os.path.expanduser("~")
        target = os.path.expanduser(target)
        if not os.path.isabs(target):
            target = os.path.join(session.cwd, target)
        target = os.path.normpath(target)
        if os.path.isdir(target):
            session.cwd = target
            return "", "", 0
        return "", f"cd: {target}: No such file or directory", 1

    try:
        result = subprocess.run(
            cmd_str,
            shell=True,
            cwd=session.cwd,
            env=session.env,
            capture_output=True,
            text=True,
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1
