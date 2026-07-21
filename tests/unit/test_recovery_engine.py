"""
Unit tests for ai.recovery_engine.
"""

from ai.recovery_engine import RecoveryEngine


def test_initial_state() -> None:
    engine = RecoveryEngine()

    assert engine.max_retries == 3
    assert engine.retry_count == 0
    assert engine.last_error is None
    assert engine.can_retry
    assert engine.retries_remaining == 3


def test_record_failure() -> None:
    engine = RecoveryEngine()

    engine.record_failure("Failure")

    assert engine.retry_count == 1
    assert engine.last_error == "Failure"
    assert engine.retries_remaining == 2


def test_reset() -> None:
    engine = RecoveryEngine()

    engine.record_failure("Error")
    engine.reset()

    assert engine.retry_count == 0
    assert engine.last_error is None
    assert engine.can_retry


def test_retry_limit() -> None:
    engine = RecoveryEngine(max_retries=2)

    engine.record_failure("A")
    engine.record_failure("B")

    assert not engine.can_retry
    assert engine.retries_remaining == 0


def test_run_success_first_try() -> None:
    engine = RecoveryEngine()

    calls = {"count": 0}

    def operation() -> None:
        calls["count"] += 1

    assert engine.run(operation)
    assert calls["count"] == 1
    assert engine.retry_count == 0


def test_run_success_after_retry() -> None:
    engine = RecoveryEngine(max_retries=3)

    calls = {"count": 0}

    def operation() -> None:
        calls["count"] += 1
        if calls["count"] < 2:
            raise RuntimeError("Temporary failure")

    assert engine.run(operation)
    assert calls["count"] == 2
    assert engine.retry_count == 1


def test_run_failure() -> None:
    engine = RecoveryEngine(max_retries=2)

    calls = {"count": 0}

    def operation() -> None:
        calls["count"] += 1
        raise RuntimeError("Always fails")

    assert not engine.run(operation)
    assert calls["count"] == 2
    assert engine.retry_count == 2
    assert engine.last_error == "Always fails"


def test_retries_remaining() -> None:
    engine = RecoveryEngine(max_retries=5)

    engine.record_failure("A")
    engine.record_failure("B")

    assert engine.retries_remaining == 3


def test_last_error_updated() -> None:
    engine = RecoveryEngine()

    engine.record_failure("First")
    engine.record_failure("Second")

    assert engine.last_error == "Second"
