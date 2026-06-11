"""Ex03: 属性协议。

涵盖：``__getattr__`` 代理、``__setattr__`` 验证、``__getattribute__`` 拦截。
"""
from __future__ import annotations

from typing import Any, ClassVar


class Proxy:
    """代理类：把属性访问转发给 ``target``。

    例：

    >>> class User:
    ...     name = "alice"
    ...     age = 30
    >>> p = Proxy(User())
    >>> p.name       # "alice"
    >>> p.unknown     # AttributeError
    """

    def __init__(self, target: object) -> None:
        # TODO: 保存 target
        ...

    def __getattr__(self, name: str) -> Any:
        # TODO
        ...


class StrictAttributes:
    """严格类：所有属性必须**先声明**才能赋值，否则抛 ``AttributeError``。

    用 ``__init__`` 列出"允许"的属性名（用 ``__slots__`` 的方式手动）：
    """

    def __init__(self, allowed: list[str], **kwargs: Any) -> None:
        # TODO: 初始化允许的属性名 + 根据 kwargs 赋值
        ...

    def __setattr__(self, name: str, value: Any) -> None:
        # TODO: 校验 name 是否在 allowed 中
        ...


class Frozen:
    """冻结对象：第一次 ``__setattr__`` 之后所有修改抛 ``AttributeError``。

    提示：在 ``__init__`` 期间要"绕过"冻结逻辑。
    """

    def __init__(self, **kwargs: Any) -> None:
        # TODO
        ...

    def __setattr__(self, name: str, value: Any) -> None:
        # TODO
        ...


class LoggingAttributes:
    """记录所有属性访问。

    ``LoggingAttributes.access_log`` 是类级别 ``list[str]``，记录形如：
    - ``"get x"``（``obj.x``）
    - ``"set x = 5"``
    - ``"get unknown"``（``__getattr__`` 兜底）
    """

    access_log: ClassVar[list[str]] = []

    def __getattribute__(self, name: str) -> Any:
        # TODO
        ...

    def __getattr__(self, name: str) -> Any:
        # TODO: 记录 "get unknown"
        ...

    def __setattr__(self, name: str, value: Any) -> None:
        # TODO
        ...
