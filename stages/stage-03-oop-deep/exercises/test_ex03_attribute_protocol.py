"""Ex03 测试。"""
import pytest

from .ex03_attribute_protocol import (
    Frozen,
    LoggingAttributes,
    Proxy,
    StrictAttributes,
)


class TestProxy:
    def test_basic(self) -> None:
        class Target:
            name = "alice"
            age = 30

        p = Proxy(Target())
        assert p.name == "alice"
        assert p.age == 30

    def test_unknown_raises(self) -> None:
        class Target:
            pass

        p = Proxy(Target())
        with pytest.raises(AttributeError):
            _ = p.unknown

    def test_callable_proxy(self) -> None:
        class Target:
            def greet(self, who):
                return f"hi {who}"

        p = Proxy(Target())
        assert p.greet("bob") == "hi bob"

    def test_target_unaffected(self) -> None:
        class Target:
            x = 1

        target = Target()
        p = Proxy(target)
        with pytest.raises(AttributeError):
            _ = p.missing
        # 不影响 target
        assert target.x == 1


class TestStrictAttributes:
    def test_allowed(self) -> None:
        s = StrictAttributes(["name", "age"], name="alice", age=30)
        assert s.name == "alice"
        assert s.age == 30

    def test_disallowed_raises(self) -> None:
        s = StrictAttributes(["name"])
        with pytest.raises(AttributeError):
            s.foo = 1

    def test_overwrite_allowed(self) -> None:
        s = StrictAttributes(["x"], x=1)
        s.x = 2
        assert s.x == 2


class TestFrozen:
    def test_first_set_works(self) -> None:
        f = Frozen()
        f.x = 1
        assert f.x == 1

    def test_subsequent_set_raises(self) -> None:
        f = Frozen()
        f.x = 1
        with pytest.raises(AttributeError):
            f.x = 2

    def test_init_kwargs(self) -> None:
        f = Frozen(name="alice", age=30)
        assert f.name == "alice"
        with pytest.raises(AttributeError):
            f.age = 31


class TestLoggingAttributes:
    def test_get_set(self) -> None:
        LoggingAttributes.access_log.clear()
        obj = LoggingAttributes()
        obj.x = 1
        _ = obj.x
        _ = obj.y
        assert "set x = 1" in LoggingAttributes.access_log
        assert "get x" in LoggingAttributes.access_log
        assert "get unknown" in LoggingAttributes.access_log
