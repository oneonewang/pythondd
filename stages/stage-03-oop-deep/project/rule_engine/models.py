"""数据模型。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuleResult:
    """单条规则执行结果。"""

    rule_name: str
    passed: bool
    message: str = ""

    def __bool__(self) -> bool:                       # 便于 if rule_result: ...
        return self.passed
