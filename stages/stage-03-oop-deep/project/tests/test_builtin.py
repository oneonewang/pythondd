"""内置规则测试。"""

from rule_engine.builtin_rules import RangeCheck, RequiredField, TypeCheck


class TestRequiredField:
    def test_present(self) -> None:
        rule = RequiredField(field="name")
        result = rule.evaluate({"name": "alice", "age": 30})
        assert result.passed
        assert result.rule_name == "required_field"

    def test_missing(self) -> None:
        rule = RequiredField(field="email")
        result = rule.evaluate({"name": "alice"})
        assert not result.passed
        assert "email" in result.message

    def test_empty_string(self) -> None:
        rule = RequiredField(field="name")
        result = rule.evaluate({"name": ""})
        assert not result.passed

    def test_none(self) -> None:
        rule = RequiredField(field="name")
        result = rule.evaluate({"name": None})
        assert not result.passed

    def test_explain(self) -> None:
        rule = RequiredField(field="email")
        assert "email" in rule.explain()


class TestTypeCheck:
    def test_correct_type(self) -> None:
        rule = TypeCheck("age", int)
        result = rule.evaluate({"age": 30})
        assert result.passed

    def test_wrong_type(self) -> None:
        rule = TypeCheck("age", int)
        result = rule.evaluate({"age": "30"})
        assert not result.passed

    def test_subclass_ok(self) -> None:
        class MyInt(int):
            pass

        rule = TypeCheck("n", int)
        assert rule.evaluate({"n": MyInt(5)}).passed

    def test_missing_field(self) -> None:
        rule = TypeCheck("age", int)
        result = rule.evaluate({})
        assert not result.passed

    def test_explain(self) -> None:
        rule = TypeCheck("age", int)
        assert "age" in rule.explain() and "int" in rule.explain()


class TestRangeCheck:
    def test_in_range(self) -> None:
        rule = RangeCheck("age", min_val=0, max_val=150)
        assert rule.evaluate({"age": 30}).passed

    def test_below(self) -> None:
        rule = RangeCheck("age", min_val=0, max_val=150)
        assert not rule.evaluate({"age": -1}).passed

    def test_above(self) -> None:
        rule = RangeCheck("age", min_val=0, max_val=150)
        assert not rule.evaluate({"age": 200}).passed

    def test_only_min(self) -> None:
        rule = RangeCheck("score", min_val=0)
        assert rule.evaluate({"score": 100}).passed
        assert not rule.evaluate({"score": -1}).passed

    def test_only_max(self) -> None:
        rule = RangeCheck("score", max_val=100)
        assert rule.evaluate({"score": 50}).passed
        assert not rule.evaluate({"score": 200}).passed

    def test_explain(self) -> None:
        rule = RangeCheck("age", min_val=0, max_val=150)
        text = rule.explain()
        assert "0" in text and "150" in text
