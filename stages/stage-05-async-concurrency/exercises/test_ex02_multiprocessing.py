"""Ex02 测试。"""
import pytest

from .ex02_multiprocessing import (
    cpu_heavy,
    is_prime,
    parallel_count_primes,
    run_cpu_parallel,
)


class TestRunCpuParallel:
    def test_basic(self) -> None:
        items = [1, 2, 3, 4]
        results = sorted(run_cpu_parallel(cpu_heavy, items, max_workers=2))
        assert results == sorted([cpu_heavy(x) for x in items])

    def test_empty(self) -> None:
        assert run_cpu_parallel(cpu_heavy, [], max_workers=2) == []


class TestIsPrime:
    @pytest.mark.parametrize(
        "n,expected",
        [
            (0, False),
            (1, False),
            (2, True),
            (3, True),
            (4, False),
            (5, True),
            (9, False),
            (11, True),
            (25, False),
            (97, True),
        ],
    )
    def test_cases(self, n: int, expected: bool) -> None:
        assert is_prime(n) is expected


class TestParallelCountPrimes:
    def test_small(self) -> None:
        # 0..100 质数: 2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97 = 25
        assert parallel_count_primes(100, 20) == 25

    def test_empty(self) -> None:
        assert parallel_count_primes(0, 10) == 0

    def test_two(self) -> None:
        assert parallel_count_primes(2, 1) == 1
