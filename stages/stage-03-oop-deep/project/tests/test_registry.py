"""Registry 测试。"""
import pytest
from rule_engine.protocols import Rule
from rule_engine.registry import RuleRegistry


class _MyRule:
    name = "my_rule"
    priority = 50

    def __init__(self, msg="default"):
        self.msg = msg

    def evaluate(self, data):
        from rule_engine.models import RuleResult

        return RuleResult(rule_name=self.name, passed=True, message=self.msg)

    def explain(self):
        return f"my rule: {self.msg}"


class TestRegistry:
    def test_register_instance(self) -> None:
        r = RuleRegistry()
        rule = _MyRule()
        r.register(rule)
        assert "my_rule" in r
        assert r.get("my_rule") is rule

    def test_register_class(self) -> None:
        r = RuleRegistry()
        r.register_class(_MyRule)
        assert "my_rule" in r
        assert isinstance(r.get("my_rule"), _MyRule)

    def test_overwrite(self) -> None:
        r = RuleRegistry()
        r.register(_MyRule(msg="first"))
        r.register(_MyRule(msg="second"))
        assert r.get("my_rule").msg == "second"

    def test_all_sorted_by_priority(self) -> None:
        r = RuleRegistry()

        class LowPri:
            name = "low"
            priority = 1

            def evaluate(self, data):
                from rule_engine.models import RuleResult

                return RuleResult("low", True)

            def explain(self):
                return "low"

        class HighPri:
            name = "high"
            priority = 100

            def evaluate(self, data):
                from rule_engine.models import RuleResult

                return RuleResult("high", True)

            def explain(self):
                return "high"

        r.register_class(HighPri)
        r.register_class(LowPri)
        names = [rule.name for rule in r.all()]
        assert names == ["high", "low"]

    def test_get_missing_raises(self) -> None:
        r = RuleRegistry()
        with pytest.raises(KeyError):
            r.get("missing")

    def test_isinstance_rule(self) -> None:
        r = RuleRegistry()
        r.register_class(_MyRule)
        assert isinstance(r.get("my_rule"), Rule)        # Protocol 检查
