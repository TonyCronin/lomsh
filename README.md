# lomsh — Local Model Shell

A simple shell harness for local models. Not a replacement for OpenCode or Goose — those are great tools. This is something smaller: a real bash REPL where a locally-hosted model is one keystroke away.

Point it at any OpenAI-compatible endpoint — vLLM, LiteLLM, Ollama, a LiteLLM proxy in front of a DGX. Single-shot calls, no autonomous looping, no cloud dependency. You run the commands, the model advises.

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

**With pipx (recommended — isolated, available everywhere):**
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

## Configuration

Set via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOMSH_BASE_URL` | `http://100.91.143.63:4000/v1` | OpenAI-compatible API endpoint |
| `LOMSH_MODEL` | `Qwen Coder` | Model name |
| `LOMSH_API_KEY` | `sk-sovereign-local` | API key (ignored by most local servers) |
| `LOMSH_MAX_CTX` | `100000` | Max tokens sent as context |

Any OpenAI-compatible endpoint works — vLLM, LiteLLM, Ollama, a LiteLLM proxy in front of your DGX.

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
