"""Ex05 测试。"""
import json

import pytest

from .ex05_slots_and_mixin import (
    Point2D,
    Point3D,
    User,
    estimate_memory_savings,
)


class TestPoint2D:
    def test_basic(self) -> None:
        p = Point2D(3, 4)
        assert p.x == 3
        assert p.y == 4
        assert repr(p) == "Point2D(3, 4)"

    def test_no_dict(self) -> None:
        p = Point2D(1, 2)
        with pytest.raises(AttributeError):
            _ = p.__dict__

    def test_cannot_add_attr(self) -> None:
        p = Point2D(1, 2)
        with pytest.raises(AttributeError):
            p.z = 3


class TestPoint3D:
    def test_inherits(self) -> None:
        p = Point3D(1, 2, 3)
        assert p.x == 1 and p.y == 2 and p.z == 3
        assert repr(p) == "Point3D(1, 2, 3)"

    def test_no_dict(self) -> None:
        p = Point3D(1, 2, 3)
        with pytest.raises(AttributeError):
            _ = p.__dict__


class TestUserWithMixins:
    def test_to_json(self) -> None:
        u = User("alice", 30)
        data = json.loads(u.to_json())
        assert data == {"name": "alice", "age": 30}

    def test_eq(self) -> None:
        a = User("alice", 30)
        b = User("alice", 30)
        c = User("bob", 30)
        assert a == b
        assert a != c

    def test_hash(self) -> None:
        a = User("alice", 30)
        b = User("alice", 30)
        assert hash(a) == hash(b)
        s = {a, b}
        assert len(s) == 1

    def test_repr(self) -> None:
        u = User("alice", 30)
        assert repr(u) == "User(name='alice', age=30)"


class TestMemorySavings:
    def test_slots_saves_memory(self) -> None:
        class WithDict:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        class WithSlots:
            __slots__ = ("x", "y")

            def __init__(self, x, y):
                self.x = x
                self.y = y

        savings = estimate_memory_savings(WithDict, WithSlots, n=10_000)
        assert savings > 0        # slots 一定更省
