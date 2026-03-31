# Lomsh — Requirements

## Core philosophy

Shell-first. The user is in a real shell. The AI is a guest, not the host.

## Functional requirements

### Shell
- FR-01: Execute arbitrary shell commands via subprocess
- FR-02: Intercept `cd` and maintain persistent cwd across commands
- FR-03: Display stdout and stderr with distinct styling
- FR-04: Show non-zero exit codes when stderr is empty

### Agent
- FR-05: Invoke the agent with `> message` prefix
- FR-06: Single-shot call only — no autonomous looping or sub-agents
- FR-07: Agent receives full session context: cwd, os, all commands + output, all prior exchanges
- FR-08: Stream response tokens to terminal as they arrive
- FR-09: Display a thinking animation while waiting for first token
- FR-10: Show per-call token counts (in, out) and running session total after each response

### Session context
- FR-11: Maintain a rolling transcript of the last 50 commands and agent exchanges
- FR-12: Transcript is the single source of truth — commands and conversations are interleaved chronologically

### Persistent stats
- FR-13: Accumulate token usage across sessions in `~/.lomsh_stats.json`
- FR-14: `:alltime` command displays lifetime totals including current session

### Built-ins
- FR-15: `exit` / `quit` — save stats and exit
- FR-16: `:help` — command reference
- FR-17: `:tokens` — session token totals
- FR-18: `:alltime` — all-time token totals
- FR-19: `:clear` — clear screen
- FR-20: `:history` — print session transcript

## Non-functional requirements

- NFR-01: Single Python file runnable without install (`python lomsh/cli.py` not required, but package must install cleanly)
- NFR-02: Installable via `pipx` for isolation
- NFR-03: Any OpenAI-compatible endpoint (vLLM, LiteLLM, Ollama, OpenAI)
- NFR-04: Configurable entirely via environment variables
- NFR-05: Arrow keys and command history work in the REPL (readline)
- NFR-06: True-color ANSI palette — no dependency on terminal theme
- NFR-07: macOS is the primary supported platform; Linux is also supported. Tab completion must work on both (macOS uses libedit, Linux uses GNU readline — detect and bind accordingly).

## Testing requirements

- TR-01: Pure functions tested without mocking the model
- TR-02: `_process_stream` extracted as a pure function and tested with fake chunks
- TR-03: `--live` flag for integration tests against the real endpoint (skipped in CI)
- TR-04: Stats persistence tested against a temp file (not `~/.lomsh_stats.json`)
- TR-05: CI runs tests on Python 3.9, 3.11, 3.12 via GitHub Actions

## Out of scope (v1)

- Agent tools (file write, run_command)
- Context compression above 128k
- Multiple named model profiles
- TUI (prompt_toolkit)
