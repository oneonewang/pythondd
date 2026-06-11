"""规则引擎：执行注册表中的全部规则，聚合结果。"""
from __future__ import annotations

from dataclasses import dataclass, field

from .models import RuleResult
from .registry import RuleRegistry


@dataclass
class EngineReport:
    """引擎对一份输入的完整报告。"""

    passed: bool
    results: list[RuleResult] = field(default_factory=list)

    @property
    def failures(self) -> list[RuleResult]:
        return [r for r in self.results if not r.passed]

    def summary(self) -> str:
        n_pass = sum(1 for r in self.results if r.passed)
        n_fail = len(self.failures)
        return f"{n_pass} passed, {n_fail} failed"


class RuleEngine:
    """按规则优先级执行，返回聚合报告。"""

    def __init__(self, registry: RuleRegistry) -> None:
        # TODO
        ...

    def evaluate(self, data: dict) -> EngineReport:
        # TODO: 跑所有规则，收集结果
        raise NotImplementedError

    def explain(self, name: str) -> str:
        # TODO: 取出指定规则的 explain() 输出
        raise NotImplementedError

    def list_rules(self) -> list[str]:
        # TODO: 按优先级返回规则名
        raise NotImplementedError
