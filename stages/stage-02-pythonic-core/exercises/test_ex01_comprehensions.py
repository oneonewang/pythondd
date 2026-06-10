"""Ex01 测试。"""
import pytest

from .ex01_comprehensions import (
    cartesian_product,
    first_n_squares,
    index_above_threshold,
    matrix_flatten,
    pair_with_index,
    transpose,
    unique_lengths,
    word_lengths,
)


class TestMatrixFlatten:
    def test_basic(self) -> None:
        assert matrix_flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    def test_irregular(self) -> None:
        assert matrix_flatten([[1], [2, 3, 4], [5, 6]]) == [1, 2, 3, 4, 5, 6]

    def test_empty(self) -> None:
        assert matrix_flatten([]) == []


class TestTranspose:
    def test_3x3(self) -> None:
        assert transpose([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],
        ]

    def test_1x1(self) -> None:
        assert transpose([[42]]) == [[42]]


class TestWordLengths:
    def test_basic(self) -> None:
        assert word_lengths(["hi", "hello", "ok", "world"]) == {
            "hello": 5,
            "world": 5,
        }

    def test_empty(self) -> None:
        assert word_lengths([]) == {}


class TestUniqueLengths:
    def test_basic(self) -> None:
        assert unique_lengths(["a", "bb", "ccc", "dd"]) == {1, 2, 3}


class TestFirstNSquares:
    @pytest.mark.parametrize(
        "n,expected",
        [
            (0, []),
            (1, [0]),
            (5, [0, 1, 4, 9, 16]),
        ],
    )
    def test_cases(self, n: int, expected: list[int]) -> None:
        assert first_n_squares(n) == expected


class TestCartesianProduct:
    def test_basic(self) -> None:
        assert cartesian_product([1, 2], [3, 4]) == [(1, 3), (1, 4), (2, 3), (2, 4)]

    def test_empty(self) -> None:
        assert cartesian_product([], [1, 2]) == []
        assert cartesian_product([1, 2], []) == []


class TestIndexAboveThreshold:
    def test_basic(self) -> None:
        assert index_above_threshold([10, 5, 20, 3, 15], 7) == {0: 10, 2: 20, 4: 15}

    def test_none(self) -> None:
        assert index_above_threshold([1, 2, 3], 10) == {}


class TestPairWithIndex:
    def test_basic(self) -> None:
        assert pair_with_index(["a", "b", "c"]) == [(0, "a"), (1, "b"), (2, "c")]

    def test_empty(self) -> None:
        assert pair_with_index([]) == []
