"""Colour palette and ANSI style helpers."""

RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"


def _fg(hex_color: str) -> str:
    """ANSI true-color foreground for a hex string like #fb8500."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m"


def _bg(hex_color: str) -> str:
    """ANSI true-color background for a hex string like #023047."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"\033[48;2;{r};{g};{b}m"


# ── palette ───────────────────────────────────────────────────────────────────
C_PROMPT  = _fg("#fb8500")   # 1 — Orange        — prompt
C_OUTPUT  = _fg("#fb8500")   # 2 — Orange        — command stdout
C_AGENT   = _fg("#219ebc")   # 3 — Teal          — agent response text
C_AGENTBG = _bg("#023047")   # 4 — Midnight Navy — agent response background
C_STATS   = _fg("#8ecae6")   # 5 — Sky Blue      — token stats
C_ERROR   = _fg("#ee6c4d")   # 6 — Burnt Orange  — errors


def prompt_style(s: str) -> str: return f"{BOLD}{C_PROMPT}{s}{RESET}"
def output_style(s: str) -> str: return f"{C_OUTPUT}{s}{RESET}"
def agent_style(s: str)  -> str: return f"{C_AGENTBG}{C_AGENT}{s}{RESET}"
def stats_style(s: str)  -> str: return f"{DIM}{C_STATS}{s}{RESET}"
def error_style(s: str)  -> str: return f"{C_ERROR}{s}{RESET}"
def dim(s: str)          -> str: return f"{DIM}{s}{RESET}"
def bold(s: str)         -> str: return f"{BOLD}{s}{RESET}"
