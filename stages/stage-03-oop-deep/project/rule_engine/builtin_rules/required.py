"""内置规则：必填字段检查。"""
from __future__ import annotations

from ..models import RuleResult


class RequiredField:
    """检查 ``data[field]`` 存在且非空。

    构造时通过 ``__init__`` 接受 ``field`` / ``fields``（多个字段）。

    用 ``name`` / ``priority`` 作为**类属性**，所有实例共享（同一规则的不同字段用不同实例）。
    """

    name = "required_field"
    priority = 100

    def __init__(self, field: str | None = None, fields: list[str] | None = None) -> None:
        # TODO: 存 field / fields（至少有一个）
        ...

    def evaluate(self, data: dict) -> RuleResult:
        # TODO: 检查字段是否存在且非空
        raise NotImplementedError

    def explain(self) -> str:
        # TODO
        raise NotImplementedError
