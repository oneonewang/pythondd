"""Ex05: ``__slots__`` 与 Mixin。

涵盖：``__slots__`` 内存优化、Mixin 组合、协作式多继承。
"""
from __future__ import annotations

import sys


class Point2D:
    """用 ``__slots__`` 的 2D 点。"""

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        # TODO
        ...

    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        # TODO
        ...


class Point3D(Point2D):
    """3D 点，也用 ``__slots__``（消除 ``__dict__``）。"""

    __slots__ = ("z",)

    def __init__(self, x: float, y: float, z: float) -> None:
        # TODO: 调 super().__init__
        ...

    def __repr__(self) -> str:
        return f"Point3D({self.x}, {self.y}, {self.z})"


class JsonMixin:
    """Mixin：提供 ``to_json()`` / ``from_json()``。

    要求子类有 ``__init__`` 能从 ``dict`` 构造。
    """

    def to_json(self) -> str:
        # TODO: 用 self.__dict__ 转 JSON
        ...


class EqMixin:
    """Mixin：用 ``__dict__`` 全部比较。"""

    def __eq__(self, other: object) -> bool:
        # TODO
        ...

    def __hash__(self) -> int:
        # TODO: 排好序的 items hash
        ...


class ReprMixin:
    """Mixin：默认 ``__repr__`` 输出 ``ClassName(field1=..., field2=...)``。"""

    def __repr__(self) -> str:
        # TODO
        ...


class User(JsonMixin, EqMixin, ReprMixin):
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


def estimate_memory_savings(cls_with_dict: type, cls_with_slots: type, n: int = 100_000) -> int:
    """构造 ``n`` 个实例，返回"用 dict 的总大小" - "用 slots 的总大小"。

    用 ``sys.getsizeof`` 估算。
    """
    # TODO
    raise NotImplementedError
