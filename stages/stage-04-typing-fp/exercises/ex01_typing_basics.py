"""Ex01: typing 基础。

涵盖：``list[T]``、``Optional``、``TypedDict``、``Literal``、``NewType``。
"""
from __future__ import annotations

from typing import Literal, NewType, TypedDict

# 类型别名
Level = Literal["INFO", "WARN", "ERROR"]
UserId = NewType("UserId", int)


class UserDict(TypedDict):
    """表示从 JSON 读出的 user 形状。"""

    name: str
    age: int
    email: str


def parse_user(data: dict) -> UserDict | None:
    """把 ``data`` 解析成 :class:`UserDict`。

    要求字段：``name`` (str), ``age`` (int), ``email`` (str)。
    字段缺失或类型不符返回 ``None``（不抛异常）。
    """
    # TODO: 实现
    raise NotImplementedError


def filter_by_level(
    records: list[dict],
    level: Level,
) -> list[dict]:
    """返回 ``records`` 中 ``level`` 字段等于 ``level`` 的项。"""
    # TODO: 实现
    raise NotImplementedError


def make_user_id(n: int) -> UserId:
    """把 ``int`` 包成 :class:`UserId`。"""
    # TODO: 实现
    raise NotImplementedError


def user_label(uid: UserId, name: str) -> str:
    """返回 ``"#{uid}: {name}"``。"""
    # TODO: 实现
    raise NotImplementedError


def safe_first(xs: list[int] | None) -> int | None:
    """``xs`` 为 None 或空时返回 None；否则返回 ``xs[0]``。"""
    # TODO: 实现
    raise NotImplementedError
