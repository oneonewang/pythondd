"""Ex04: ABC 与 Protocol。

涵盖：``abc.ABCMeta``、``typing.Protocol``、``runtime_checkable``。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable

# ==================== ABC ====================


class Shape(ABC):
    """抽象 Shape。

    必须实现 ``area`` / ``perimeter`` 才能实例化。
    """

    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...

    def describe(self) -> str:
        return f"{type(self).__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Rectangle(Shape):
    """矩形，长宽存到 ``self.width`` / ``self.height``。"""

    def __init__(self, width: float, height: float) -> None:
        # TODO
        ...

    def area(self) -> float:
        # TODO
        ...

    def perimeter(self) -> float:
        # TODO
        ...


class Circle(Shape):
    """圆，半径 ``self.radius``。"""

    def __init__(self, radius: float) -> None:
        # TODO
        ...

    def area(self) -> float:
        # TODO
        ...

    def perimeter(self) -> float:
        # TODO
        ...


# ==================== Protocol ====================


@runtime_checkable
class SupportsClose(Protocol):
    """任何有 ``close() -> None`` 方法的对象。"""

    def close(self) -> None: ...


@runtime_checkable
class SupportsRead(Protocol):
    """任何有 ``read() -> str`` 方法的对象。"""

    def read(self) -> str: ...


class FileLike:
    """同时有 read/close 两种方法的示例。"""

    def __init__(self, data: str) -> None:
        self.data = data
        self.closed = False

    def read(self) -> str:
        # TODO
        ...

    def close(self) -> None:
        # TODO: 标记 closed=True
        ...


def close_all(things: list[SupportsClose]) -> None:
    """调用所有对象的 ``close()``。"""
    for t in things:
        t.close()


def total_length(readables: list[SupportsRead]) -> int:
    """返回所有对象 ``read()`` 返回的字符串总长。"""
    # TODO
    raise NotImplementedError
