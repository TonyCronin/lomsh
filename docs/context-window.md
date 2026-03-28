# Context Window

## What is the context window?

Every time you call the model with `>`, lomsh sends your entire session — every command you ran, every output, every previous exchange — as context. The model reads all of it before responding.

The context window is the maximum amount of text that can be sent in a single call. It's measured in tokens (roughly 1 token ≈ 0.75 words).

## Two limits to know

| Setting | Env var | Default | What it controls |
|---------|---------|---------|-----------------|
| Context sent | `LOMSH_MAX_CTX` | 100,000 | Max tokens of session history sent to the model |
| Response length | `LOMSH_MAX_RESPONSE` | 40,000 | Max tokens the model can reply with |

These are independent. A 128k context window means the total of both must fit within 128k.

## Setting your context size

Find out your model's context window — it's listed on the model card (Ollama, Hugging Face, etc.). Then set accordingly:

```bash
# Example: 128k context model (e.g. Qwen2.5-Coder-32B)
export LOMSH_MAX_CTX=100000       # session history sent to model
export LOMSH_MAX_RESPONSE=28000   # leaves headroom within 128k total

# Example: 32k context model (e.g. smaller Qwen or Mistral)
export LOMSH_MAX_CTX=24000
export LOMSH_MAX_RESPONSE=8000

# Example: 8k context model (smaller/older models)
export LOMSH_MAX_CTX=6000
export LOMSH_MAX_RESPONSE=2000
```

Add your chosen values to `~/.zshrc` so they persist:

```bash
echo 'export LOMSH_MAX_CTX=100000' >> ~/.zshrc
echo 'export LOMSH_MAX_RESPONSE=28000' >> ~/.zshrc
source ~/.zshrc
```

## Rule of thumb

```
LOMSH_MAX_CTX + LOMSH_MAX_RESPONSE < your model's context window
```

Leave a small buffer (a few thousand tokens) for the system prompt lomsh adds automatically.

## Common model context windows

| Model | Context window | Suggested MAX_CTX | Suggested MAX_RESPONSE |
|-------|---------------|-------------------|------------------------|
| Qwen2.5-Coder 7B–72B | 128k | 100,000 | 28,000 |
| Llama 3.2 3B / 8B | 128k | 100,000 | 28,000 |
| Mistral 7B | 32k | 24,000 | 8,000 |
| Phi-3 Mini | 128k | 100,000 | 28,000 |
| DeepSeek-Coder 6.7B | 16k | 12,000 | 4,000 |

When in doubt, check the model's Hugging Face or Ollama page — context window is always listed.

## What happens when you exceed the limit?

lomsh doesn't crash — the oldest session history is simply not included in the call. The most recent commands and exchanges are always kept. You'll see a warning in a future release when you're approaching the limit.
