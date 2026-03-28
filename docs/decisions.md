# Architecture Decision Records

---

## ADR-001 — Shell-first, not agent-first
**Status:** accepted

**Context:** Most AI coding tools (OpenCode, Cursor, etc.) make the agent the primary actor and shell a tool it controls.

**Decision:** Invert this. The REPL is a real shell. The agent is invoked on demand with `>` and returns control immediately. No autonomous loops, no sub-agents.

**Consequences:** Users retain full control of sequencing. The agent can advise but cannot act without the user executing its suggestions.

---

## ADR-002 — Session transcript as shared context
**Status:** accepted

**Context:** The agent needs context to be useful. Options: (a) send only recent commands, (b) send full conversation history separately, (c) interleave everything.

**Decision:** A single rolling transcript interleaves shell commands, their output, and agent exchanges in chronological order. This is what the agent sees — it mirrors what the user sees.

**Consequences:** The agent has genuine session context. No separate "chat history" to manage.

---

## ADR-003 — OpenAI-compatible API only
**Status:** accepted

**Context:** Built for Qwen 80B on DGX Spark via LiteLLM proxy, but should work with any local or remote model.

**Decision:** Use the `openai` Python SDK pointed at a configurable `base_url`. No model-specific SDKs.

**Consequences:** Works with vLLM, LiteLLM, Ollama (OpenAI-compat mode), and OpenAI itself. Model switching is an env var change.

---

## ADR-004 — Don't test `call_agent` with full mocks
**Status:** accepted

**Context:** `call_agent` is a thin wrapper around the OpenAI SDK streaming API. Mocking the full SDK is brittle and doesn't test real behaviour.

**Decision:** Extract `_process_stream(stream)` as a pure function that takes any iterable of chunk-like objects. Test this with fake chunks. Test all session/stats/colour logic directly. Add a `--live` integration test flag for real endpoint verification.

**Consequences:** High coverage on pure logic, no fragile SDK mocks, real endpoint test available when needed.

---

## ADR-005 — pipx as the recommended install method
**Status:** accepted

**Context:** lomsh is a CLI tool, not a library. Installing into the user's global Python risks dependency conflicts.

**Decision:** Recommend `pipx install` which gives lomsh its own isolated venv but exposes the `lomsh` command globally.

**Consequences:** Clean install, no conflicts, works across machines with one command.

---

## ADR-006 — Persist token stats in `~/.lomsh_stats.json`
**Status:** accepted

**Context:** Users want to track cumulative token usage across sessions.

**Decision:** On exit (clean or Ctrl+C), add session totals to a JSON file in the home directory. `:alltime` reads and displays this.

**Consequences:** Simple, portable, human-readable. File survives reinstalls. No database dependency.

---

## ADR-007 — Rename smarsh → lomsh
**Status:** accepted

**Context:** The original working name "smarsh" (smart shell) was a placeholder. As the project matured toward a GitHub release, a more precise name was needed that communicated what it actually is.

**Decision:** Rename to **lomsh** — Local Model Shell. All three defining characteristics (local, model, shell) are present in the name. Pronounced "lomsh".

**Consequences:** Package name, command, env vars (`LOMSH_*`), stats file (`~/.lomsh_stats.json`), and GitHub repo URL all updated. The old `smarsh.py` single-file prototype remains in the repo root as a historical artefact until first release.
