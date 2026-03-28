# Context Window

## What is the context window?

Every time you call the model with `>`, lomsh sends your entire session — every command you ran, every output, every previous exchange — as context. The model reads all of it before responding.

The context window is the maximum amount of text that can be sent in a single call. It's measured in tokens (roughly 1 token ≈ 0.75 words).

## One setting to know

| Setting | Env var | Default | What it controls |
|---------|---------|---------|-----------------|
| Context sent | `LOMSH_MAX_CTX` | 100,000 | Max tokens of session history sent to the model |

The model's response is never truncated by lomsh — whatever the model generates streams fully to your terminal.

## Setting your context size

Find out your model's context window — it's listed on the model card (Ollama, Hugging Face, etc.). Set `LOMSH_MAX_CTX` to leave some headroom for the system prompt lomsh adds automatically (a few thousand tokens).

```bash
# 128k context model (e.g. Qwen2.5-Coder, Llama 3.2)
export LOMSH_MAX_CTX=120000

# 32k context model (e.g. Mistral 7B)
export LOMSH_MAX_CTX=28000

# 8k context model (smaller/older models)
export LOMSH_MAX_CTX=6000
```

Add to `~/.zshrc` so it persists:

```bash
echo 'export LOMSH_MAX_CTX=120000' >> ~/.zshrc
source ~/.zshrc
```

## Common model context windows

| Model | Context window | Suggested LOMSH_MAX_CTX |
|-------|---------------|--------------------------|
| Qwen2.5-Coder 7B–72B | 128k | 120,000 |
| Llama 3.2 3B / 8B | 128k | 120,000 |
| Mistral 7B | 32k | 28,000 |
| Phi-3 Mini | 128k | 120,000 |
| DeepSeek-Coder 6.7B | 16k | 12,000 |

When in doubt, check the model's Hugging Face or Ollama page — context window is always listed.

## What happens when you exceed the limit?

lomsh doesn't crash — the oldest session history is simply not included in the call. The most recent commands and exchanges are always kept.
