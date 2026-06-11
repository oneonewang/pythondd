"""注册表：管理规则的注册、查询、列出。"""
from __future__ import annotations

from collections.abc import Iterator

from .protocols import Rule


class RuleRegistry:
    """一个注册表实例管理若干规则类。"""

    def __init__(self) -> None:
        # TODO: 用 dict 存 name -> rule instance
        ...

    def register(self, rule: Rule) -> None:
        """注册一个**实例**。同名规则会覆盖。"""
        # TODO
        ...

    def register_class(self, rule_cls: type) -> None:
        """注册一个**类**（自动实例化）。"""
        # TODO
        ...

    def get(self, name: str) -> Rule:
        # TODO
        raise NotImplementedError

    def all(self) -> list[Rule]:
        """返回所有规则实例，按 priority 降序。"""
        # TODO
        raise NotImplementedError

    def __contains__(self, name: str) -> bool: ...
    def __iter__(self) -> Iterator[Rule]: ...
    def __len__(self) -> int: ...


_default_registry: RuleRegistry | None = None


def get_default_registry() -> RuleRegistry:
    """进程级单例。"""
    global _default_registry
    if _default_registry is None:
        _default_registry = RuleRegistry()
        # 触发内置规则注册
        from . import builtin_rules  # noqa: F401  触发 __init__.py 注册
    return _default_registry


def reset_default_registry() -> None:
    """测试用：重置单例。"""
    global _default_registry
    _default_registry = None
