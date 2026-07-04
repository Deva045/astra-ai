"""
Application Paths
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ASSETS = ROOT / "assets"

DATABASE = ROOT / "database"

MODELS = ROOT / "models"

LOGS = ROOT / "logs"

CACHE = ROOT / "cache"