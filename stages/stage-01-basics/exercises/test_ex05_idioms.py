"""Ex05 测试。"""
import pytest

from .ex05_idioms import (
    build_index,
    count_upper,
    find_evens,
    first_n,
    has_positive,
    is_empty,
    swap_dict,
    total,
)


class TestTotal:
    @pytest.mark.parametrize(
        "nums,expected",
        [
            ([1, 2, 3], 6),
            ([], 0),
            ([-1, 1], 0),
            ([10], 10),
        ],
    )
    def test_cases(self, nums, expected) -> None:
        assert total(nums) == expected


class TestFindEvens:
    def test_basic(self) -> None:
        assert find_evens([1, 2, 3, 4, 5, 6]) == [2, 4, 6]

    def test_empty(self) -> None:
        assert find_evens([]) == []

    def test_no_even(self) -> None:
        assert find_evens([1, 3, 5]) == []


class TestIsEmpty:
    def test_empty_list(self) -> None:
        assert is_empty([]) is True

    def test_non_empty(self) -> None:
        assert is_empty([1]) is False

    def test_empty_string(self) -> None:
        assert is_empty("") is True

    def test_empty_dict(self) -> None:
        assert is_empty({}) is True


class TestFirstN:
    def test_basic(self) -> None:
        assert first_n(["a", "b", "c", "d"], 2) == ["a", "b"]

    def test_n_larger(self) -> None:
        assert first_n(["a", "b"], 10) == ["a", "b"]

    def test_zero(self) -> None:
        assert first_n(["a", "b"], 0) == []

    def test_empty(self) -> None:
        assert first_n([], 3) == []


class TestHasPositive:
    def test_true(self) -> None:
        assert has_positive([-1, 0, 1]) is True

    def test_false(self) -> None:
        assert has_positive([-1, 0, -2]) is False

    def test_empty(self) -> None:
        assert has_positive([]) is False


class TestCountUpper:
    def test_basic(self) -> None:
        assert count_upper("HelloWorld") == 2

    def test_no_upper(self) -> None:
        assert count_upper("hello") == 0

    def test_all_upper(self) -> None:
        assert count_upper("HELLO") == 5

    def test_empty(self) -> None:
        assert count_upper("") == 0

    def test_mixed(self) -> None:
        assert count_upper("aBcDeFg") == 3


class TestBuildIndex:
    def test_basic(self) -> None:
        assert build_index([("a", 1), ("b", 2), ("a", 3)]) == {
            "a": [1, 3],
            "b": [2],
        }

    def test_empty(self) -> None:
        assert build_index([]) == {}


class TestSwapDict:
    def test_basic(self) -> None:
        assert swap_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}

    def test_empty(self) -> None:
        assert swap_dict({}) == {}
