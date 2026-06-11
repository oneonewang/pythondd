"""Ex02 测试。"""
from .ex02_generics import Pair, Stack, first_or_default, map_list, timer


class TestStack:
    def test_empty(self) -> None:
        s = Stack[int]()
        assert s.is_empty()
        assert len(s) == 0

    def test_push_pop(self) -> None:
        s: Stack[int] = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        assert len(s) == 3
        assert s.pop() == 3
        assert s.pop() == 2
        assert s.pop() == 1
        assert s.is_empty()

    def test_peek(self) -> None:
        s: Stack[str] = Stack()
        s.push("a")
        s.push("b")
        assert s.peek() == "b"
        assert len(s) == 2                  # peek 不弹

    def test_pop_empty(self) -> None:
        s: Stack[int] = Stack()
        import pytest

        with pytest.raises(IndexError):
            s.pop()


class TestPair:
    def test_basic(self) -> None:
        p: Pair[str, int] = Pair("age", 30)
        assert p.key == "age"
        assert p.value == 30

    def test_swap(self) -> None:
        p: Pair[str, int] = Pair("age", 30)
        p2 = p.swap()
        assert p2.key == 30
        assert p2.value == "age"

    def test_repr(self) -> None:
        p: Pair[str, int] = Pair("a", 1)
        s = repr(p)
        assert "a" in s and "1" in s


class TestMapList:
    def test_basic(self) -> None:
        assert map_list([1, 2, 3], lambda x: x * 2) == [2, 4, 6]

    def test_empty(self) -> None:
        assert map_list([], lambda x: x) == []

    def test_type_change(self) -> None:
        assert map_list([1, 2, 3], str) == ["1", "2", "3"]


class TestFirstOrDefault:
    def test_non_empty(self) -> None:
        assert first_or_default([1, 2, 3], 0) == 1

    def test_empty(self) -> None:
        assert first_or_default([], 99) == 99

    def test_generator(self) -> None:
        assert first_or_default((x for x in [10, 20]), -1) == 10


class TestTimer:
    def test_returns_same_result(self) -> None:
        @timer
        def add(a: int, b: int) -> int:
            return a + b

        assert add(1, 2) == 3

    def test_passes_kwargs(self) -> None:
        @timer
        def f(x: int, y: int = 10) -> int:
            return x * y

        assert f(3, y=4) == 12
