"""Main REPL entry point."""

import os
import glob
import readline

readline.set_completer_delims(' \t\n;')
if readline.__doc__ and 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

from . import __version__
from .colours import prompt_style, output_style, error_style, stats_style, agent_style, dim, bold, C_PROMPT, C_AGENT, RESET
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


# LOM and SH split across two colour columns
# Orange (#fb8500) for LOM, Teal (#219ebc) for SH
_LOM = [
    "█      █████  ██ ██",
    "█      █   █  █ █ █",
    "█      █   █  █   █",
    "█████  █████  █   █",
]
_SH = [
    "  ████   █   █",
    "  █      █   █",
    "   ███   █████",
    "  ████   █   █",
]


def _print_logo():
    print()   # top padding
    print()
    for lom, sh in zip(_LOM, _SH):
        print(f"  {C_PROMPT}{lom}{RESET}{C_AGENT}{sh}{RESET}")
    print()
    # subtitle — colours match letter groupings
    print(f"  {C_PROMPT}LOcal Model {RESET}{C_AGENT}Shell{RESET}")
    print()


def main():
    session = Session()

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

    readline.set_completer(_path_completer)

    _print_logo()
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
