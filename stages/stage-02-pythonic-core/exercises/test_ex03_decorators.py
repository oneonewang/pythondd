"""Ex03 测试。"""
import time

import pytest

from .ex03_decorators import (
    CountCalls,
    logger,
    retry,
    slow,
    timer,
    validate_int,
)


class TestTimer:
    def test_records_elapsed(self) -> None:
        @timer
        def s():
            time.sleep(0.01)
            return 42

        result = s()
        assert result == 42
        assert s.last_elapsed >= 0.01

    def test_preserves_name(self) -> None:
        @timer
        def my_func():
            pass

        assert my_func.__name__ == "my_func"


class TestLogger:
    def test_logs_call_and_result(self, capsys) -> None:
        @logger
        def add(a, b):
            return a + b

        add(1, 2)
        captured = capsys.readouterr()
        assert "call add(1, 2)" in captured.out
        assert "-> 3" in captured.out

    def test_preserves_kwargs(self, capsys) -> None:
        @logger
        def f(x, y=10):
            return x * y

        f(2, y=3)
        captured = capsys.readouterr()
        assert "y=3" in captured.out


class TestRetry:
    def test_succeeds_after_failures(self) -> None:
        attempts = {"n": 0}

        @retry(times=3, delay=0.0)
        def flaky():
            attempts["n"] += 1
            if attempts["n"] < 3:
                raise ValueError("transient")
            return "ok"

        assert flaky() == "ok"
        assert attempts["n"] == 3

    def test_eventual_failure_reraises(self) -> None:
        @retry(times=2, delay=0.0)
        def always_fails():
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError, match="boom"):
            always_fails()

    def test_delay(self) -> None:
        @retry(times=2, delay=0.05)
        def f():
            raise ValueError()

        start = time.perf_counter()
        with pytest.raises(ValueError):
            f()
        assert time.perf_counter() - start >= 0.05


class TestValidateInt:
    def test_valid(self) -> None:
        @validate_int(int, float)
        def f(a, b):
            return a + b

        assert f(1, 2.0) == 3.0

    def test_invalid_raises(self) -> None:
        @validate_int(int, float)
        def f(a):
            return a

        with pytest.raises(TypeError):
            f("not a number")

    def test_no_args(self) -> None:
        @validate_int(int, float)
        def f():
            return 0

        assert f() == 0


class TestCountCalls:
    def test_counts(self) -> None:
        @CountCalls
        def f():
            return "x"

        assert f() == "x"
        assert f() == "x"
        assert f() == "x"
        assert f.count == 3

    def test_preserves_name(self) -> None:
        @CountCalls
        def my_func():
            pass

        assert my_func.__name__ == "my_func"

    def test_passes_args(self) -> None:
        @CountCalls
        def add(a, b):
            return a + b

        assert add(1, 2) == 3
        assert add.count == 1


class TestSlow:
    def test_returns_n(self) -> None:
        assert slow(5) == 5
