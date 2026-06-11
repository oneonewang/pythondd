"""内置规则：字段类型检查。"""
from __future__ import annotations

from ..models import RuleResult


class TypeCheck:
    """检查 ``data[field]`` 是 ``expected_type``（或它的一个子类）。"""

    name = "type_check"
    priority = 90

    def __init__(self, field: str, expected_type: type) -> None:
        # TODO
        ...

    def evaluate(self, data: dict) -> RuleResult:
        # TODO
        raise NotImplementedError

    def explain(self) -> str:
        # TODO
        raise NotImplementedError
