# lomsh — Local Model Shell

A shell harness built specifically for local models.

Cloud-first agent tools (OpenCode, Goose — great products) assume a fast, reliable API. Local models are different. They're slower, occasionally flaky, and don't need an autonomous loop running on top of them. lomsh is built for that reality.

**What makes it stable for local models:**
- Single-shot calls only — one request, one response, done. No looping, no sub-agents, nothing running in the background
- No timeouts — local models can be slow; lomsh waits
- Full output — responses up to 40k tokens by default, configurable up to your model's full context window
- No cloud dependency — works entirely offline once your model is running

You stay in a real shell running real commands. The model is one keystroke away when you need it.

```
~/projects/myapp $ ls
src/  tests/  pyproject.toml

~/projects/myapp $ > why are my pytest imports failing?
────────────────────────────────────────────────────────────
Looks like the package isn't installed in editable mode...
────────────────────────────────────────────────────────────
  ↑ 412 in  ↓ 183 out  Total: 595
```

## Install

**With uv (recommended):**
```bash
uv tool install git+https://github.com/TonyCronin/lomsh.git
uv tool update-shell   # adds lomsh to your PATH — only needed once
```

**With pipx:**
```bash
pipx install git+https://github.com/TonyCronin/lomsh.git
```

**With pip:**
```bash
pip install git+https://github.com/TonyCronin/lomsh.git
```

**From source:**
```bash
git clone https://github.com/TonyCronin/lomsh.git
cd lomsh
pip install -e .
```

## Run

```bash
lomsh
```

## Usage

Everything you type runs as a shell command. To talk to the assistant, prefix with `>`:

```
~/code $ pwd
/Users/you/code

~/code $ cd myproject

~/myproject $ git status
On branch main...

~/myproject $ > what does this output mean?
```

The assistant sees your full session — every command you ran and its output — as context.

### Built-in commands

| Command | Description |
|---------|-------------|
| `> message` | Send a message to the assistant |
| `exit` / `quit` | Leave lomsh |
| `:help` | Show this reference |
| `:tokens` | Token usage for this session |
| `:alltime` | Cumulative token usage across all sessions |
| `:clear` | Clear the screen |
| `:history` | Print session history |

## Setting up a model

lomsh works with Ollama, LM Studio, vLLM, or a LiteLLM proxy. Step-by-step setup for each: [docs/models.md](docs/models.md)

## Context window

lomsh sends your full session as context on every call. How to configure it for your model: [docs/context-window.md](docs/context-window.md)

## Configuration reference

| Variable | Default | Description |
|----------|---------|-------------|
| `LOMSH_BASE_URL` | `http://100.91.143.63:4000/v1` | OpenAI-compatible API endpoint |
| `LOMSH_MODEL` | `Qwen Coder` | Model name |
| `LOMSH_API_KEY` | `sk-sovereign-local` | API key (ignored by most local servers) |
| `LOMSH_MAX_CTX` | `100000` | Max tokens sent as context |
| `LOMSH_MAX_RESPONSE` | `40000` | Max tokens in model response |

## Colours

lomsh uses a custom true-colour palette. Details and how to change it: [docs/colours.md](docs/colours.md)

## Development

```bash
git clone https://github.com/TonyCronin/lomsh.git
cd lomsh
pip install -e .
make test
```

## Architecture

```
lomsh/
  colours.py   — ANSI palette and style functions
  config.py    — env-var configuration
  stats.py     — persistent token counters (~/.lomsh_stats.json)
  shell.py     — Session state, run_command, cd interception
  agent.py     — Spinner, _process_stream, call_agent
  cli.py       — REPL loop, built-in commands
```
