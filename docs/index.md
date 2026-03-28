---
title: Home
nav_order: 1
---

<pre class="lomsh-logo"><span class="lom">█      █████  ██ ██</span><span class="sh">  ████   █   █</span>
<span class="lom">█      █   █  █ █ █</span><span class="sh">  █      █   █</span>
<span class="lom">█      █   █  █   █</span><span class="sh">   ███   █████</span>
<span class="lom">█████  █████  █   █</span><span class="sh">  ████   █   █</span></pre>

<p class="lomsh-subtitle"><span class="lom">LOcal Model </span><span class="sh">Shell</span></p>

# lomsh — Local Model Shell

A shell harness built specifically for local models.

Running a local model is a different experience — slower responses, occasional hiccups, no cloud fallback. lomsh is designed around that reality from the ground up. If you're looking for a full agentic coding assistant, check out [OpenCode](https://github.com/sst/opencode) or [Goose](https://github.com/block/goose) — great tools for that job.

**Built for local:**
- Single-shot calls only — one request, one response, done. No looping, no sub-agents, nothing running in the background
- No timeouts — local models can be slow; lomsh waits
- Full output — the complete model response streams to your terminal, nothing truncated
- Works entirely offline once your model is running

You stay in a real shell running real commands. The model is one keystroke away when you need it.

---

## Quick start

```bash
# Install
uv tool install git+https://github.com/TonyCronin/lomsh.git
uv tool update-shell   # add lomsh to PATH — once only

# Run
lomsh
```

Then in lomsh, prefix any message with `>` to talk to the assistant:

```
~ $ ls
src/  tests/  pyproject.toml

~ $ > why are my pytest imports failing?
────────────────────────────────────────────────────────────
Looks like the package isn't installed in editable mode...
────────────────────────────────────────────────────────────
  ↑ 412 in  ↓ 183 out  Total: 595
```

---

## Built-in commands

| Command | Description |
|---------|-------------|
| `> message` | Send a message to the assistant |
| `exit` / `quit` | Leave lomsh |
| `:help` | Show command reference |
| `:tokens` | Token usage for this session |
| `:alltime` | Cumulative tokens across all sessions |
| `:clear` | Clear the screen |
| `:history` | Print session history |

---

## Install options

**uv (recommended):**
```bash
uv tool install git+https://github.com/TonyCronin/lomsh.git
uv tool update-shell
```

**pipx:**
```bash
pipx install git+https://github.com/TonyCronin/lomsh.git
```

**From source:**
```bash
git clone https://github.com/TonyCronin/lomsh.git
cd lomsh
pip install -e .
```
