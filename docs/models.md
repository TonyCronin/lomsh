# Model Setup

lomsh needs a local model to talk to. Pick the path that matches your setup.

---

## Path 1 — Ollama (easiest, any Mac or Linux machine)

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

## Path 2 — LM Studio (GUI, good for Windows/Mac)

[Download LM Studio](https://lmstudio.ai), search for a model in the app, download it, then start the local server from the Developer tab.

```bash
export LOMSH_BASE_URL=http://localhost:1234/v1
export LOMSH_MODEL=your-model-name   # as shown in LM Studio
lomsh
```

---

## Path 3 — vLLM (GPU server)

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

## Path 4 — LiteLLM proxy (advanced, multiple models)

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
| `LOMSH_MAX_CTX` | `100000` | Max tokens of session history sent to the model |
