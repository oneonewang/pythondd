"""Ex02 测试。"""

from .ex02_iterators_generators import (
    Cycle,
    chunked,
    fibonacci,
    flatten,
    running_total,
    sliding_window,
    take,
)


class TestFibonacci:
    def test_zero(self) -> None:
        assert list(fibonacci(0)) == []

    def test_one(self) -> None:
        assert list(fibonacci(1)) == [0]

    def test_seven(self) -> None:
        assert list(fibonacci(7)) == [0, 1, 1, 2, 3, 5, 8]

    def test_is_generator(self) -> None:
        import types

        assert isinstance(fibonacci(5), types.GeneratorType)


class TestTake:
    def test_basic(self) -> None:
        assert take(3, [1, 2, 3, 4, 5]) == [1, 2, 3]

    def test_zero(self) -> None:
        assert take(0, [1, 2, 3]) == []

    def test_more_than_available(self) -> None:
        assert take(10, [1, 2]) == [1, 2]

    def test_works_with_generators(self) -> None:
        assert take(4, (x * 2 for x in range(10))) == [0, 2, 4, 6]


class TestChunked:
    def test_even(self) -> None:
        assert list(chunked([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]

    def test_odd(self) -> None:
        assert list(chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]

    def test_empty(self) -> None:
        assert list(chunked([], 3)) == []

    def test_size_one(self) -> None:
        assert list(chunked([1, 2, 3], 1)) == [[1], [2], [3]]


class TestFlatten:
    def test_basic(self) -> None:
        assert list(flatten([1, [2, [3, 4], 5], 6])) == [1, 2, 3, 4, 5, 6]

    def test_already_flat(self) -> None:
        assert list(flatten([1, 2, 3])) == [1, 2, 3]

    def test_empty(self) -> None:
        assert list(flatten([])) == []


class TestSlidingWindow:
    def test_basic(self) -> None:
        assert list(sliding_window([1, 2, 3, 4, 5], 3)) == [
            (1, 2, 3),
            (2, 3, 4),
            (3, 4, 5),
        ]

    def test_k_equals_length(self) -> None:
        assert list(sliding_window([1, 2, 3], 3)) == [(1, 2, 3)]

    def test_k_too_large(self) -> None:
        assert list(sliding_window([1, 2], 3)) == []

    def test_k_one(self) -> None:
        assert list(sliding_window([1, 2, 3], 1)) == [(1,), (2,), (3,)]


class TestRunningTotal:
    def test_basic(self) -> None:
        assert list(running_total([1, 2, 3, 4])) == [1, 3, 6, 10]

    def test_empty(self) -> None:
        assert list(running_total([])) == []

    def test_negatives(self) -> None:
        assert list(running_total([5, -2, -3, 10])) == [5, 3, 0, 10]


class TestCycle:
    def test_basic(self) -> None:
        c = Cycle([1, 2, 3])
        it = iter(c)
        assert [next(it) for _ in range(7)] == [1, 2, 3, 1, 2, 3, 1]

    def test_take_from_cycle(self) -> None:
        c = Cycle(["a", "b"])
        it = iter(c)
        assert [next(it) for _ in range(5)] == ["a", "b", "a", "b", "a"]
