from pathlib import Path

# ==========================
# AI MODEL
# ==========================

MODEL = "qwen2.5-coder:7b"

# ==========================
# PROJECT PATHS
# ==========================

PROJECT_ROOT = Path(__file__).parent.resolve()

WORKSPACE = PROJECT_ROOT / "workspace"

LOGS = PROJECT_ROOT / "logs"

MEMORY = PROJECT_ROOT / "memory"

# ==========================
# AGENT SETTINGS
# ==========================

MAX_ITERATIONS = 20

DEBUG = True

# ==========================
# SECURITY
# ==========================

ALLOW_TERMINAL = True

ALLOW_DELETE = True