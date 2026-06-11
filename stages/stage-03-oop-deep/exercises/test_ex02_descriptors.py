"""Ex02 测试。"""
import pytest

from .ex02_descriptors import Tracer, Typed, validated


class TestTyped:
    def test_valid_set(self) -> None:
        class U:
            name = Typed(str)

        u = U()
        u.name = "alice"
        assert u.name == "alice"

    def test_invalid_type_raises(self) -> None:
        class U:
            age = Typed(int)

        u = U()
        with pytest.raises(TypeError):
            u.age = "thirty"

    def test_independent_instances(self) -> None:
        class U:
            x = Typed(int)

        a, b = U(), U()
        a.x = 1
        b.x = 2
        assert a.x == 1
        assert b.x == 2


class TestTracer:
    def test_records_reads_writes(self) -> None:
        Tracer.log.clear()

        class T:
            x = Tracer("x")

        t = T()
        t.x = 10
        _ = t.x
        _ = t.x
        assert Tracer.log == ["x write 10", "x read", "x read"]

    def test_isolation_across_instances(self) -> None:
        Tracer.log.clear()

        class T:
            x = Tracer("x")

        a, b = T(), T()
        a.x = 1
        b.x = 2
        assert Tracer.log == ["x write 1", "x write 2"]


class TestValidated:
    def test_within_range(self) -> None:
        class Score:
            value = validated(min=0, max=100)

        s = Score()
        s.value = 50
        assert s.value == 50

    def test_below_min(self) -> None:
        class Score:
            value = validated(min=0, max=100)

        s = Score()
        with pytest.raises(ValueError):
            s.value = -1

    def test_above_max(self) -> None:
        class Score:
            value = validated(min=0, max=100)

        s = Score()
        with pytest.raises(ValueError):
            s.value = 200

    def test_no_constraints(self) -> None:
        class Box:
            x = validated()

        b = Box()
        b.x = "anything"           # 没约束就放过
        assert b.x == "anything"
