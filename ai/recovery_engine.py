"""
Recovery engine for Astra AI.

Provides retry and recovery functionality for operations that may fail.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RecoveryEngine:
    """Handles retry attempts for recoverable operations."""

    max_retries: int = 3
    retry_count: int = 0
    last_error: str | None = None

    def reset(self) -> None:
        """Reset the recovery state."""
        self.retry_count = 0
        self.last_error = None

    @property
    def retries_remaining(self) -> int:
        """Return the number of retries remaining."""
        return max(0, self.max_retries - self.retry_count)

    @property
    def can_retry(self) -> bool:
        """Return True if another retry is allowed."""
        return self.retry_count < self.max_retries

    def record_failure(self, message: str) -> None:
        """Record a failed attempt."""
        self.retry_count += 1
        self.last_error = message

    def run(self, operation) -> bool:
        """
        Execute an operation with retry support.

        Returns True if the operation succeeds, otherwise False.
        """
        self.reset()

        while self.can_retry:
            try:
                operation()
                return True
            except Exception as exc:
                self.record_failure(str(exc))

        return False
