"""Ex05 测试。"""
import pytest

from .ex05_functools import (
    LetterGrade,
    SquareStats,
    cached_factorial,
    factorial_via_reduce,
    format_value,
    lru_power,
    make_doubler,
)


class TestCachedFactorial:
    def test_basic(self) -> None:
        assert cached_factorial(5) == 120
        assert cached_factorial(10) == 3628800

    def test_zero(self) -> None:
        assert cached_factorial(0) == 1


class TestLruPower:
    def test_basic(self) -> None:
        assert lru_power(2, 10) == 1024
        assert lru_power(3, 3) == 27


class TestMakeDoubler:
    def test_basic(self) -> None:
        doubler = make_doubler(2)
        assert doubler(5) == 10
        assert doubler(0) == 0

    def test_triple(self) -> None:
        tripler = make_doubler(3)
        assert tripler(5) == 15


class TestFactorialReduce:
    def test_basic(self) -> None:
        assert factorial_via_reduce(5) == 120
        assert factorial_via_reduce(0) == 1


class TestFormatValue:
    def test_int(self) -> None:
        assert format_value(42) == "42"

    def test_float(self) -> None:
        assert format_value(3.14159) == "3.14"

    def test_str(self) -> None:
        assert format_value("hi") == '"hi"'

    def test_list(self) -> None:
        assert format_value([1, 2, 3]) == "[1, 2, 3]"
        assert format_value([1, "x", 1.5]) == '[1, "x", 1.50]'

    def test_unsupported(self) -> None:
        with pytest.raises(NotImplementedError):
            format_value({1, 2})


class TestSquareStats:
    def test_mean(self) -> None:
        s = SquareStats([1, 2, 3, 4, 5])
        assert s.mean == 3.0

    def test_stdev(self) -> None:
        s = SquareStats([1, 2, 3, 4, 5])
        assert s.stdev == pytest.approx(1.414, rel=1e-2)

    def test_cached(self) -> None:
        s = SquareStats([1, 2, 3])
        _ = s.mean
        # 第二次访问应该不重算
        assert "mean" in s.__dict__


class TestLetterGrade:
    def test_eq(self) -> None:
        assert LetterGrade("A") == LetterGrade("A")

    def test_lt(self) -> None:
        assert LetterGrade("A") > LetterGrade("B")
        assert LetterGrade("F") < LetterGrade("C")

    def test_sort(self) -> None:
        grades = [LetterGrade("B"), LetterGrade("A"), LetterGrade("F")]
        grades.sort()
        assert [g.letter for g in grades] == ["F", "B", "A"]

    def test_invalid(self) -> None:
        with pytest.raises(ValueError):
            LetterGrade("Z")
