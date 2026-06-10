"""Ex05 测试。"""
import pytest

from .ex05_magic_methods import Bag, Money, Repeater


class TestBag:
    def test_len(self) -> None:
        assert len(Bag([1, 1, 2, 3])) == 4
        assert len(Bag([])) == 0

    def test_iter(self) -> None:
        assert list(Bag([1, 1, 2, 3])) == [1, 1, 2, 3]

    def test_contains(self) -> None:
        b = Bag([1, 2, 3])
        assert 1 in b
        assert 99 not in b

    def test_getitem(self) -> None:
        b = Bag([1, 1, 2, 3])
        assert b[1] == 2
        assert b[2] == 1
        assert b[99] == 0

    def test_count(self) -> None:
        b = Bag([1, 1, 1, 2])
        assert b.count(1) == 3
        assert b.count(2) == 1
        assert b.count(99) == 0

    def test_eq(self) -> None:
        assert Bag([1, 1, 2]) == Bag([1, 2, 1])
        assert Bag([1, 2]) != Bag([1, 2, 3])

    def test_eq_different_type(self) -> None:
        assert Bag([1]) != [1]

    def test_hash_consistent(self) -> None:
        b1 = Bag([1, 2, 3])
        b2 = Bag([3, 2, 1])
        assert b1 == b2
        assert hash(b1) == hash(b2)

    def test_hash_usable_in_set(self) -> None:
        s = {Bag([1, 2]), Bag([1, 2]), Bag([1, 2, 3])}
        assert len(s) == 2

    def test_repr(self) -> None:
        assert repr(Bag([1, 1, 2, 3])) == "Bag([1, 1, 2, 3])"

    def test_bool(self) -> None:
        assert bool(Bag([1]))
        assert not bool(Bag([]))


class TestMoney:
    def test_repr(self) -> None:
        assert repr(Money(10, "USD")) == "10.00 USD"
        assert repr(Money(3.5, "EUR")) == "3.50 EUR"

    def test_add_same_currency(self) -> None:
        result = Money(10, "USD") + Money(5, "USD")
        assert result.amount == 15
        assert result.currency == "USD"

    def test_add_different_currency_raises(self) -> None:
        with pytest.raises(ValueError):
            Money(10, "USD") + Money(5, "EUR")

    def test_mul_scalar(self) -> None:
        result = Money(10, "USD") * 3
        assert result.amount == 30
        assert result.currency == "USD"

    def test_mul_float(self) -> None:
        result = Money(10, "USD") * 1.5
        assert result.amount == 15

    def test_eq(self) -> None:
        assert Money(10, "USD") == Money(10, "USD")
        assert Money(10, "USD") != Money(11, "USD")
        assert Money(10, "USD") != Money(10, "EUR")

    def test_lt(self) -> None:
        assert Money(10, "USD") < Money(11, "USD")
        assert not (Money(11, "USD") < Money(10, "USD"))

    def test_lt_different_currency(self) -> None:
        # 注意：NotImplemented 由 Python 解释器处理
        with pytest.raises(TypeError):
            Money(10, "USD") < Money(10, "EUR")

    def test_hash(self) -> None:
        assert hash(Money(10, "USD")) == hash(Money(10, "USD"))


class TestRepeater:
    def test_basic(self) -> None:
        r = Repeater()
        assert r() == 0
        assert r() == 1
        assert r() == 2

    def test_len(self) -> None:
        r = Repeater()
        r()
        r()
        r()
        assert len(r) == 3

    def test_repr(self) -> None:
        r = Repeater()
        r()
        r()
        r()
        assert repr(r) == "Repeater(n=3)"
