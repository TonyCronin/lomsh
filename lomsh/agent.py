"""Agent call — single-shot, streaming, no looping."""

import select
import sys
import termios
import textwrap
import threading
import time
import tty

from openai import OpenAI

from .colours import agent_style, error_style, stats_style, dim
from .shell import Session
from .stats import load_alltime

BASE_URL = None   # set from config at runtime
MODEL    = None
API_KEY  = None

BRAILLE = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


class Spinner:
    """Braille spinner in a background thread."""

    def __init__(self, label: str = "thinking"):
        self._stop   = threading.Event()
        self._label  = label
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        i = 0
        while not self._stop.is_set():
            frame = BRAILLE[i % len(BRAILLE)]
            sys.stdout.write(f"\r{agent_style(frame)} {dim(self._label)}  ")
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1

    def start(self): self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join()
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()


def _watch_for_escape(stop_event: threading.Event) -> None:
    """
    Watch stdin for Escape or Ctrl+C in raw mode.
    Sets stop_event when either is detected.
    Restores terminal state on exit.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while not stop_event.is_set():
            if select.select([sys.stdin], [], [], 0.05)[0]:
                ch = sys.stdin.read(1)
                if ch in ("\x1b", "\x03"):   # Escape or Ctrl+C
                    stop_event.set()
                    break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def _process_stream(stream) -> tuple[str, int, int]:
    """
    Consume an OpenAI streaming response.
    Returns (response_text, prompt_tokens, completion_tokens).
    Pure function — no printing, no side effects.
    """
    response_text = ""
    usage_in = usage_out = 0

    for chunk in stream:
        if hasattr(chunk, "usage") and chunk.usage is not None:
            usage_in  = chunk.usage.prompt_tokens
            usage_out = chunk.usage.completion_tokens

        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta
        if not delta or not delta.content:
            continue

        response_text += delta.content

    return response_text, usage_in, usage_out


def call_agent(user_msg: str, session: Session) -> str:
    """
    Single-shot call to the local model.
    Streams response to stdout. Updates session token totals.
    Returns the full response text, or "" on error.
    """
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

    system_prompt = textwrap.dedent(f"""
        You are Lomsh — a DevOps and software development specialist embedded in the user's shell.
        You have full context of their current session below.

        Be direct and practical. When writing code or scripts, include them inline in your response.
        When you suggest a command to run, format it clearly so the user can see exactly what to execute.
        You do not run commands yourself — the user runs them. Your job is to advise, explain, and write code.

        {session.build_context()}
    """).strip()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_msg},
    ]

    stop_event  = threading.Event()
    watcher     = threading.Thread(target=_watch_for_escape, args=(stop_event,), daemon=True)
    spinner     = Spinner()
    spinner.start()
    watcher.start()

    first_token = True
    streamed    = []
    interrupted = False
    usage_in = usage_out = 0

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
            stream_options={"include_usage": True},
            max_tokens=None,
        )

        for chunk in stream:
            if stop_event.is_set():
                interrupted = True
                break

            if hasattr(chunk, "usage") and chunk.usage is not None:
                usage_in  = chunk.usage.prompt_tokens
                usage_out = chunk.usage.completion_tokens

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            if not delta or not delta.content:
                continue

            if first_token:
                spinner.stop()
                print(agent_style("─" * 60))
                first_token = False

            text = delta.content
            streamed.append(text)
            sys.stdout.write(agent_style(text))
            sys.stdout.flush()

    except KeyboardInterrupt:
        interrupted = True

    except Exception as e:
        stop_event.set()
        spinner.stop()
        print(error_style(f"\n[lomsh] model error: {e}"))
        return ""

    finally:
        stop_event.set()   # unblock the watcher thread

    if first_token:
        spinner.stop()

    if interrupted:
        print()
        print(agent_style("─" * 60))
        print(dim("  (interrupted)"))

    print()
    session.total_in  += usage_in
    session.total_out += usage_out
    at_in, at_out = load_alltime()
    alltime_total = at_in + at_out + session.total_in + session.total_out
    stats = (
        f"  ↑ {usage_in:,} in  "
        f"↓ {usage_out:,} out  "
        f"Session: {session.total_in + session.total_out:,}  "
        f"All time: {alltime_total:,}"
    )
    print(agent_style("─" * 60))
    print(stats_style(stats))

    return "".join(streamed)
