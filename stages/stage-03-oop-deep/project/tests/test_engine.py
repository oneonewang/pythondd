"""Engine 测试。"""
import pytest
from rule_engine.engine import RuleEngine
from rule_engine.models import RuleResult
from rule_engine.registry import RuleRegistry, reset_default_registry


def make_passing_rule(name: str, priority: int = 50):
    class _R:
        pass

    r = _R()
    r.name = name
    r.priority = priority

    def evaluate(data):
        return RuleResult(name, True, f"{name} ok")

    def explain():
        return f"explain {name}"

    r.evaluate = evaluate
    r.explain = explain
    return r


def make_failing_rule(name: str, priority: int = 50):
    r = make_passing_rule(name, priority)

    def evaluate(data):
        return RuleResult(name, False, f"{name} fail")

    r.evaluate = evaluate
    return r


class TestEngine:
    def test_all_pass(self) -> None:
        registry = RuleRegistry()
        registry.register(make_passing_rule("a", 100))
        registry.register(make_passing_rule("b", 50))
        engine = RuleEngine(registry)
        report = engine.evaluate({})
        assert report.passed
        assert len(report.results) == 2
        assert report.summary() == "2 passed, 0 failed"

    def test_continues_after_failure(self) -> None:
        registry = RuleRegistry()
        registry.register(make_passing_rule("a"))
        registry.register(make_failing_rule("b"))
        registry.register(make_passing_rule("c"))
        engine = RuleEngine(registry)
        report = engine.evaluate({})
        assert not report.passed
        assert len(report.results) == 3
        assert len(report.failures) == 1

    def test_priority_order(self) -> None:
        registry = RuleRegistry()
        registry.register(make_passing_rule("low", 1))
        registry.register(make_passing_rule("high", 100))
        engine = RuleEngine(registry)
        report = engine.evaluate({})
        assert [r.rule_name for r in report.results] == ["high", "low"]

    def test_explain(self) -> None:
        registry = RuleRegistry()
        registry.register(make_passing_rule("foo"))
        engine = RuleEngine(registry)
        assert engine.explain("foo") == "explain foo"

    def test_explain_missing(self) -> None:
        registry = RuleRegistry()
        engine = RuleEngine(registry)
        with pytest.raises(KeyError):
            engine.explain("nope")

    def test_list_rules(self) -> None:
        registry = RuleRegistry()
        registry.register(make_passing_rule("a", 10))
        registry.register(make_passing_rule("b", 20))
        engine = RuleEngine(registry)
        assert engine.list_rules() == ["b", "a"]


class TestBuiltinRulesIntegration:
    def test_default_registry_has_builtins(self) -> None:
        from rule_engine.builtin_rules import (  # noqa: F401
            RangeCheck,
            RequiredField,
            TypeCheck,
        )
        from rule_engine.registry import get_default_registry

        registry = get_default_registry()
        names = [r.name for r in registry.all()]
        assert "required_field" in names
        assert "type_check" in names
        assert "range_check" in names

    def test_full_pipeline(self) -> None:
        from rule_engine.builtin_rules import (
            RangeCheck,
            RequiredField,
            TypeCheck,
        )
        from rule_engine.registry import get_default_registry

        # 构造一个"配置化"的注册表
        reset_default_registry()
        registry = get_default_registry()
        registry.register(RequiredField(fields=["name", "age"]))
        registry.register(TypeCheck("age", int))
        registry.register(RangeCheck("age", min_val=0, max_val=150))

        engine = RuleEngine(registry)
        report = engine.evaluate({"name": "alice", "age": 30})
        assert report.passed

        report = engine.evaluate({"name": "", "age": 200})
        assert not report.passed
        assert len(report.failures) == 3
