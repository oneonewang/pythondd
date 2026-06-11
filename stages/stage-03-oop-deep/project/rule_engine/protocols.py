"""规则协议：定义"什么样的对象算一个规则"。

不强制继承——任何实现下列属性/方法的类都算。
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from .models import RuleResult


@runtime_checkable
class Rule(Protocol):
    """规则接口。"""

    name: str
    priority: int

    def evaluate(self, data: dict) -> RuleResult: ...

    def explain(self) -> str: ...
