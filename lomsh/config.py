"""Runtime configuration — read from environment, fall back to DGX Spark defaults."""

import os

BASE_URL = os.environ.get("LOMSH_BASE_URL", "http://100.91.143.63:4000/v1")
MODEL    = os.environ.get("LOMSH_MODEL",    "Qwen Coder")
API_KEY  = os.environ.get("LOMSH_API_KEY",  "sk-sovereign-local")
MAX_CTX      = int(os.environ.get("LOMSH_MAX_CTX",     100_000))
MAX_RESPONSE = int(os.environ.get("LOMSH_MAX_RESPONSE", 40_000))
