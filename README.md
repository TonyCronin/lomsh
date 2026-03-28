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

lomsh needs a local model to talk to. Pick the path that matches your setup.

---

### Path 1 — Ollama (easiest, any Mac or Linux machine)

Ollama runs models locally with one command. No GPU required for smaller models.

```bash
# Install Ollama
brew install ollama        # macOS
# or: curl -fsSL https://ollama.com/install.sh | sh   # Linux

# Start the Ollama server
ollama serve

# Pull a model (in a new terminal tab)
ollama pull qwen2.5-coder   # good coding model, ~4GB
# or: ollama pull llama3.2  # general purpose, ~2GB
```

Then tell lomsh to use it:

```bash
export LOMSH_BASE_URL=http://localhost:11434/v1
export LOMSH_MODEL=qwen2.5-coder
lomsh
```

Add those exports to your `~/.zshrc` so you don't have to repeat them.

---

### Path 2 — LM Studio (GUI, good for Windows/Mac)

[Download LM Studio](https://lmstudio.ai), search for a model in the app, download it, then start the local server from the Developer tab.

```bash
export LOMSH_BASE_URL=http://localhost:1234/v1
export LOMSH_MODEL=your-model-name   # as shown in LM Studio
lomsh
```

---

### Path 3 — vLLM (GPU server)

For running larger models on a machine with a GPU. Requires Python and a CUDA-capable GPU.

```bash
pip install vllm
vllm serve Qwen/Qwen2.5-Coder-7B-Instruct --port 8000
```

```bash
export LOMSH_BASE_URL=http://localhost:8000/v1
export LOMSH_MODEL=Qwen/Qwen2.5-Coder-7B-Instruct
lomsh
```

---

### Path 4 — LiteLLM proxy (advanced, multiple models)

LiteLLM lets you run a proxy in front of any model — useful if you're managing several models on a DGX or remote server.

```bash
pip install litellm
litellm --model ollama/qwen2.5-coder --port 4000
```

```bash
export LOMSH_BASE_URL=http://localhost:4000/v1
export LOMSH_MODEL=qwen2.5-coder
lomsh
```

See the [LiteLLM docs](https://docs.litellm.ai) for proxying remote GPU servers.

---

## Configuration reference

| Variable | Default | Description |
|----------|---------|-------------|
| `LOMSH_BASE_URL` | `http://100.91.143.63:4000/v1` | OpenAI-compatible API endpoint |
| `LOMSH_MODEL` | `Qwen Coder` | Model name |
| `LOMSH_API_KEY` | `sk-sovereign-local` | API key (ignored by most local servers) |
| `LOMSH_MAX_CTX` | `100000` | Max tokens sent as context |

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
