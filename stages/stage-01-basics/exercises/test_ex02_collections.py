"""Ex02 测试。"""

from .ex02_collections import (
    chunk,
    dedup_preserve_order,
    group_by_first_letter,
    intersect_sorted,
    top_n_frequent,
)


class TestDedupPreserveOrder:
    def test_basic(self) -> None:
        assert dedup_preserve_order([3, 1, 3, 2, 1]) == [3, 1, 2]

    def test_empty(self) -> None:
        assert dedup_preserve_order([]) == []

    def test_no_dup(self) -> None:
        assert dedup_preserve_order([1, 2, 3]) == [1, 2, 3]

    def test_all_same(self) -> None:
        assert dedup_preserve_order([5, 5, 5]) == [5]


class TestGroupByFirstLetter:
    def test_basic(self) -> None:
        assert group_by_first_letter(["apple", "ant", "Banana"]) == {
            "a": ["apple", "ant"],
            "b": ["Banana"],
        }

    def test_empty(self) -> None:
        assert group_by_first_letter([]) == {}


class TestIntersectSorted:
    def test_basic(self) -> None:
        assert intersect_sorted([1, 2, 3, 4, 5], [2, 4, 6]) == [2, 4]

    def test_duplicates(self) -> None:
        # 1 在 a 中出现两次，b 中出现一次，结果去重为 [1, 2]
        assert intersect_sorted([1, 1, 2, 3], [1, 2, 2]) == [1, 2]

    def test_no_common(self) -> None:
        assert intersect_sorted([1, 2], [3, 4]) == []

    def test_empty(self) -> None:
        assert intersect_sorted([], [1, 2]) == []


class TestTopNFrequent:
    def test_basic(self) -> None:
        items = ["a", "b", "a", "c", "b", "a"]
        assert top_n_frequent(items, 2) == [("a", 3), ("b", 2)]

    def test_tie_break_alphabetical(self) -> None:
        items = ["x", "y", "x", "y"]
        assert top_n_frequent(items, 2) == [("x", 2), ("y", 2)]

    def test_n_larger_than_unique(self) -> None:
        items = ["a", "b"]
        assert top_n_frequent(items, 5) == [("a", 1), ("b", 1)]


class TestChunk:
    def test_even(self) -> None:
        assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test_odd(self) -> None:
        assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test_size_larger_than_list(self) -> None:
        assert chunk([1, 2], 10) == [[1, 2]]

    def test_size_one(self) -> None:
        assert chunk([1, 2, 3], 1) == [[1], [2], [3]]

    def test_empty(self) -> None:
        assert chunk([], 3) == []
