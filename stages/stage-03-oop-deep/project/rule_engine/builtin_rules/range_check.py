"""内置规则：数值范围检查。"""
from __future__ import annotations

from ..models import RuleResult


class RangeCheck:
    """检查 ``data[field]`` 在 ``[min_val, max_val]`` 之间。"""

    name = "range_check"
    priority = 80

    def __init__(
        self,
        field: str,
        min_val: float | None = None,
        max_val: float | None = None,
    ) -> None:
        # TODO
        ...

    def evaluate(self, data: dict) -> RuleResult:
        # TODO
        raise NotImplementedError

    def explain(self) -> str:
        # TODO
        raise NotImplementedError
