"""Ex03: Protocol 进阶。

涵盖：``Self``、组合 Protocol、``runtime_checkable``。
"""
from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol, Self, runtime_checkable


@runtime_checkable
class SupportsAdd(Protocol):
    """任何有 ``__add__`` 方法的对象。"""

    def __add__(self, other: SupportsAdd) -> Self: ...


@runtime_checkable
class SupportsRead(Protocol):
    def read(self) -> str: ...


@runtime_checkable
class SupportsWrite(Protocol):
    def write(self, data: str) -> int: ...


@runtime_checkable
class SupportsReadWrite(SupportsRead, SupportsWrite, Protocol):
    pass


class StrBuffer:
    """同时实现 read + write 的示例对象。"""

    def __init__(self, initial: str = "") -> None:
        self._buf = initial

    def read(self) -> str:
        return self._buf

    def write(self, data: str) -> int:
        self._buf += data
        return len(data)


def total_length(streams: Iterable[SupportsRead]) -> int:
    """所有 stream 的 ``read()`` 返回的字符串总长。"""
    # TODO
    raise NotImplementedError


def write_all(streams: Iterable[SupportsWrite], data: str) -> int:
    """把 ``data`` 写入所有 stream，返回写入总字节数。"""
    # TODO
    raise NotImplementedError


class ChainReader:
    """把多个 ``SupportsRead`` 串起来当一个用。"""

    def __init__(self, streams: Iterable[SupportsRead]) -> None:
        # TODO
        ...

    def read(self) -> str:
        # TODO
        raise NotImplementedError
