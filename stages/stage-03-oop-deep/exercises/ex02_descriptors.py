"""Ex02: 描述符。

涵盖：``__get__``/``__set__``/``__delete__``、``__set_name__``、typed property。
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any, ClassVar


class Typed:
    """类型化属性描述符：赋值时检查类型。

    用法：

    >>> class User:
    ...     name = Typed(str)
    ...     age = Typed(int)
    >>> u = User()
    >>> u.name = "alice"     # OK
    >>> u.age = "thirty"     # TypeError
    """

    def __init__(self, expected_type: type) -> None:
        # TODO
        ...

    def __set_name__(self, owner: type, name: str) -> None:
        # TODO: 保存真实存储名（私有）
        ...

    def __get__(self, obj: Any, type: type | None = None) -> Any:
        # TODO
        raise NotImplementedError

    def __set__(self, obj: Any, value: Any) -> None:
        # TODO: 检查类型，存到私有名
        ...


class Tracer:
    """追踪描述符：每次 ``get`` / ``set`` 时往 ``Tracer.log`` 追加一条记录。

    ``Tracer.log`` 是类级别的 ``list[str]``。
    """

    log: ClassVar[list[str]] = []

    def __init__(self, name: str) -> None:
        self.name = name

    def __set_name__(self, owner: type, name: str) -> None:
        # TODO
        ...

    def __get__(self, obj: Any, type: type | None = None) -> Any:
        # TODO: 记录 "<name> read"
        raise NotImplementedError

    def __set__(self, obj: Any, value: Any) -> None:
        # TODO: 记录 "<name> write <value>"
        ...


def validated(min: float | None = None, max: float | None = None) -> Callable[[Any, Any], Any]:
    """返回描述符工厂：给一个属性加上范围校验。

    用法：

    >>> class T:
    ...     score = validated(min=0, max=100)
    """

    class _Validated:
        def __set_name__(self_, owner: type, name: str) -> None:
            # TODO
            ...

        def __get__(self_, obj, type=None):
            # TODO
            raise NotImplementedError

        def __set__(self_, obj, value) -> None:
            # TODO
            ...

    return _Validated()
