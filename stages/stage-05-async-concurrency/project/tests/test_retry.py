"""retry 测试。"""
import asyncio
import time

import pytest
from async_crawler.retry import retry


class TestRetry:
    def test_succeeds_after_failures(self) -> None:
        attempts = {"n": 0}

        @retry(max_attempts=3, base_delay=0.01)
        async def flaky() -> str:
            attempts["n"] += 1
            if attempts["n"] < 3:
                raise ValueError("oops")
            return "ok"

        assert asyncio.run(flaky()) == "ok"
        assert attempts["n"] == 3

    def test_eventual_failure_raises(self) -> None:
        @retry(max_attempts=2, base_delay=0.01)
        async def always_fail() -> str:
            raise RuntimeError("nope")

        with pytest.raises(RuntimeError, match="nope"):
            asyncio.run(always_fail())

    def test_exponential_backoff(self) -> None:
        @retry(max_attempts=3, base_delay=0.1, max_delay=10.0)
        async def fail() -> None:
            raise ValueError()

        start = time.perf_counter()
        with pytest.raises(ValueError):
            asyncio.run(fail())
        # 0.1 + 0.2 = 0.3s 总等待
        elapsed = time.perf_counter() - start
        assert elapsed >= 0.25

    def test_only_catches_specified(self) -> None:
        @retry(max_attempts=3, base_delay=0.01, exceptions=(ValueError,))
        async def fail() -> None:
            raise TypeError("not caught")

        with pytest.raises(TypeError):
            asyncio.run(fail())
