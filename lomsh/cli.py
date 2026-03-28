"""Main REPL entry point."""

import os
import readline
import rlcompleter

# Tab completion — paths and python names
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")

from . import __version__
from .colours import prompt_style, output_style, error_style, stats_style, dim, bold
from .shell   import Session, run_command
from .stats   import load_alltime, save_alltime
from .agent   import call_agent
from . import agent as _agent_module
from .config  import BASE_URL, MODEL, API_KEY

# Wire config into agent module at startup
_agent_module.BASE_URL = BASE_URL
_agent_module.MODEL    = MODEL
_agent_module.API_KEY  = API_KEY

HELP_TEXT = """
lomsh commands:
  > <message>   — send a message to the AI assistant
  exit / quit   — leave lomsh
  :help         — show this help
  :tokens       — show session token totals
  :alltime      — show cumulative tokens across all sessions
  :clear        — clear the screen
  :history      — print session history
Everything else is passed to your shell.
""".strip()


def make_prompt(session: Session) -> str:
    home = os.path.expanduser("~")
    cwd  = session.cwd.replace(home, "~")
    return f"{prompt_style(cwd)} $ "


LOGO = r"""
█       ███   █   █  ████  █   █
█      █   █  ██ ██  █     █   █
█      █   █  █ █ █   ███  █████
█      █   █  █   █     █  █   █
█████   ███   █   █  ████  █   █
""".strip("\n")


def main():
    session = Session()

    print(agent_style(LOGO))
    print()
    print(dim(f"  v{__version__}  model={MODEL}  endpoint={BASE_URL}"))
    print(dim("  :help for commands  |  > to talk to the assistant"))
    print()

    while True:
        try:
            line = input(make_prompt(session))
        except (EOFError, KeyboardInterrupt):
            print()
            save_alltime(session.total_in, session.total_out)
            break

        line = line.strip()
        if not line:
            continue

        # ── built-ins ──────────────────────────────────────────────────────

        if line in ("exit", "quit"):
            save_alltime(session.total_in, session.total_out)
            break

        if line == ":help":
            print(dim(HELP_TEXT))
            continue

        if line == ":tokens":
            total = session.total_in + session.total_out
            print(stats_style(f"↑ {session.total_in:,} in  ↓ {session.total_out:,} out  Total: {total:,}"))
            continue

        if line == ":alltime":
            at_in, at_out = load_alltime()
            at_in  += session.total_in
            at_out += session.total_out
            print(stats_style(f"All time — ↑ {at_in:,} in  ↓ {at_out:,} out  Total: {at_in + at_out:,}"))
            continue

        if line == ":clear":
            os.system("clear")
            continue

        if line == ":history":
            for entry in session.history:
                if entry["type"] == "cmd":
                    print(dim(f"$ {entry['cmd']}"))
                else:
                    print(dim(f"> {entry['user']}"))
            continue

        # ── agent invocation ───────────────────────────────────────────────

        if line.startswith(">"):
            user_msg = line[1:].strip()
            if not user_msg:
                print(dim("usage: > your message to the assistant"))
                continue
            response = call_agent(user_msg, session)
            if response:
                session.add_agent(user_msg, response)
            continue

        # ── shell command ──────────────────────────────────────────────────

        stdout, stderr, rc = run_command(line, session)
        session.add_cmd(line, stdout, stderr, rc)

        if stdout:
            print(output_style(stdout), end="" if stdout.endswith("\n") else "\n")
        if stderr:
            print(error_style(stderr), end="" if stderr.endswith("\n") else "\n")
        if rc != 0 and not stderr:
            print(error_style(f"[exit {rc}]"))

    print(dim("bye"))
