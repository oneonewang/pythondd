"""Ex04 测试。"""
import pytest

from .ex04_dataclass import Counter, Money, Task, Version


class TestMoney:
    def test_basic(self) -> None:
        m = Money(10, "USD")
        assert m.amount == 10
        assert m.currency == "USD"

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError):
            Money(-1, "USD")

    def test_bad_currency_raises(self) -> None:
        with pytest.raises(ValueError):
            Money(10, "US")

    def test_frozen(self) -> None:
        from dataclasses import FrozenInstanceError

        m = Money(10, "USD")
        with pytest.raises(FrozenInstanceError):
            m.amount = 20

    def test_repr(self) -> None:
        assert "10" in repr(Money(10, "USD"))
        assert "USD" in repr(Money(10, "USD"))


class TestVersion:
    def test_parse(self) -> None:
        v = Version.parse("1.2.3")
        assert v == Version(1, 2, 3)

    def test_bump_major(self) -> None:
        v = Version(1, 2, 3)
        v2 = v.bump_major()
        assert v2 == Version(2, 0, 0)

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError):
            Version(-1, 0, 0)


class TestTask:
    def test_basic(self) -> None:
        t = Task(priority=5, title="buy milk")
        assert t.priority == 5
        assert t.title == "buy milk"
        assert t.tags == []

    def test_default_tags_independent(self) -> None:
        a = Task(priority=1, title="a")
        b = Task(priority=1, title="b")
        a.tags.append("urgent")
        assert b.tags == []                  # 没有共享 list

    def test_id_derived(self) -> None:
        t1 = Task(priority=1, title="a")
        t2 = Task(priority=1, title="b")
        assert t1._id != t2._id

    def test_order(self) -> None:
        a = Task(priority=1, title="a")
        b = Task(priority=2, title="b")
        assert a < b

    def test_sort(self) -> None:
        tasks = [Task(priority=2, title="b"), Task(priority=1, title="a"), Task(priority=3, title="c")]
        tasks.sort()
        assert [t.title for t in tasks] == ["a", "b", "c"]


class TestCounter:
    def test_basic(self) -> None:
        c = Counter(10)
        c.inc()
        assert c.value == 11

    def test_dec(self) -> None:
        c = Counter(10)
        c.dec(5)
        assert c.value == 5

    def test_default(self) -> None:
        c = Counter()
        assert c.value == 0
