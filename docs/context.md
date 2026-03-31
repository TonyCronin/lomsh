# Lomsh — Project Context

## What is this?

A smart shell. Not an AI coding tool with a terminal bolted on — the opposite. A real shell REPL where an AI assistant is available on demand.

The core insight: most of the time you want to be in a shell. Occasionally you want to ask something, get an answer, and get back to work. The AI should be a specialist you can call on, not an agent you're supervising.

## Who is it for?

Developers and DevOps engineers who live in the terminal. People who think in shell commands and want AI help without switching context.

## Hardware context

Primary development machine: DGX Spark (GX10). Local models served via LiteLLM proxy at `http://100.91.143.63:4000/v1`. Default model: Qwen 80B Coder. 128k context window.

## Current state (v0.1.1)

Working MVP:
- Real shell REPL with persistent cwd tracking
- `> message` agent invocation
- Streaming response with braille spinner
- Per-call and session token counters (session total, in/out, all-time)
- Persistent all-time token stats (`~/.lomsh_stats.json`)
- Custom colour palette (orange prompt, teal agent, midnight navy agent bg, sky blue stats, burnt orange errors)
- readline support (arrow keys, history, tab completion — macOS libedit and Linux GNU readline both handled)
- If response contains exactly one shell code block, offers to run it
- Pixel art block logo in terminal banner and docs sidebar
- Installable as `lomsh` command via uv, pipx, or pip
- macOS primary platform, Linux supported

## What's next

- Agent tools: `run_command` (agent can execute) and file read/write with diff display
- Context compression when approaching 128k
- Named model profiles in config
- `--live` integration test flag
- Version bump to `0.1.1`

## Key files

| File | Purpose |
|------|---------|
| `lomsh/cli.py` | REPL loop and built-in commands |
| `lomsh/shell.py` | Session state and command execution |
| `lomsh/agent.py` | Model call, streaming, spinner |
| `lomsh/colours.py` | Palette and ANSI style helpers |
| `lomsh/stats.py` | Persistent token counting |
| `lomsh/config.py` | Env-var configuration |
| `docs/requirements.md` | Functional and non-functional requirements |
| `docs/decisions.md` | Architecture Decision Records |

## Colour palette

| Slot | Hex | Name | Used for |
|------|-----|------|---------|
| 1 | `#fb8500` | Orange | Prompt, stdout |
| 2 | `#219ebc` | Teal | Agent response text |
| 3 | `#023047` | Midnight Navy | Agent response background |
| 4 | `#8ecae6` | Sky Blue | Token stats |
| 5 | `#ee6c4d` | Burnt Orange | Errors |
