"""
Global configuration settings for Astra AI.
"""

from __future__ import annotations

# ==========================================================
# AI Provider Configuration
# ==========================================================

# Supported:
#   "mock"
#   "ollama"
AI_PROVIDER = "mock"

# Default model to use with the selected provider.
DEFAULT_MODEL = "qwen3"

# ==========================================================
# Ollama Configuration
# ==========================================================

OLLAMA_HOST = "http://localhost:11434"

# Request timeout (seconds)
OLLAMA_TIMEOUT = 120.0

# Retry failed requests
OLLAMA_MAX_RETRIES = 3

# Retry delay (seconds)
OLLAMA_RETRY_DELAY = 1.0

# Enable streaming responses
OLLAMA_STREAM = True

# ==========================================================
# Generation Settings
# ==========================================================

TEMPERATURE = 0.7

MAX_TOKENS = 2048

TOP_P = 0.9

TOP_K = 40

REPEAT_PENALTY = 1.1

# ==========================================================
# Conversation Settings
# ==========================================================

MAX_HISTORY_MESSAGES = 20

MAX_CONTEXT_CHARS = 12000

# ==========================================================
# Logging
# ==========================================================

LOG_AI_REQUESTS = True

LOG_AI_RESPONSES = False

# ==========================================================
# Development
# ==========================================================

DEBUG = False
