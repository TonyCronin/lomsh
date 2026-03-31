# lomsh — Local Model Shell

A shell harness built specifically for local models.

Running a local model is a different experience — slower responses, occasional hiccups, no cloud fallback. lomsh is designed around that reality from the ground up. If you're looking for a full agentic coding assistant, check out [OpenCode](https://github.com/sst/opencode) or [Goose](https://github.com/block/goose) — great tools for that job.

**Built for local:**
- Single-shot calls only — one request, one response, done. No looping, no sub-agents, nothing running in the background
- No timeouts — local models can be slow; lomsh waits
- Full output — the complete model response streams to your terminal, nothing truncated
- Works entirely offline once your model is running

You stay in a real shell running real commands. The model is one keystroke away when you need it.

```
~/projects/myapp $ ls
src/  tests/  pyproject.toml

~/projects/myapp $ > why are my pytest imports failing?
────────────────────────────────────────────────────────────
Looks like the package isn't installed in editable mode...
────────────────────────────────────────────────────────────
  Tokens:  595  ↓ 412 in  ↑ 183 out  All time: 5,227
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
| `LOMSH_MAX_CTX` | `100000` | Max tokens of session history sent to the model |

## Colours

lomsh uses a custom true-colour palette. Details and how to change it: [docs/colours.md](docs/colours.md)

## Development

```bash
git clone https://github.com/TonyCronin/lomsh.git
cd lomsh
pip install -e .
make test
```

## Acknowledgements

lomsh stands on the shoulders of:

- [openai-python](https://github.com/openai/openai-python) - streaming SDK that handles the model connection
- [readline](https://tiswww.case.edu/php/chet/readline/rltop.html) / [libedit](https://thrysoee.dk/editline/) - the line editing, history, and tab completion that make the REPL feel like a real shell
- [Ollama](https://github.com/ollama/ollama), [LiteLLM](https://github.com/BerriAI/litellm), [vLLM](https://github.com/vllm-project/vllm) - the model serving layer lomsh is built for

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
