"""
Intent Recognition Engine
"""

from dataclasses import dataclass


@dataclass
class Intent:
    name: str
    confidence: float


class IntentEngine:

    def detect(self, text: str) -> Intent:

        text = text.lower().strip()

        if any(word in text for word in ["open", "launch", "start"]):
            return Intent("open_app", 0.95)

        if any(word in text for word in ["weather", "temperature"]):
            return Intent("weather", 0.95)

        if any(word in text for word in ["time", "clock"]):
            return Intent("time", 0.95)

        return Intent("chat", 0.60)