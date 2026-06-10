"""Ex03: 函数。

涵盖：默认参数、*args / **kwargs、解包、作用域、一等公民。
"""
from __future__ import annotations

from collections.abc import Callable


def make_greeting(greeting: str = "Hello", punctuation: str = "!") -> Callable[[str], str]:
    """返回一个把名字拼成问候语的函数。

    例：``f = make_greeting("Hi", "..."); f("Alice")`` -> ``"Hi, Alice..."``
    """
    # TODO: 实现
    raise NotImplementedError


def call_with_dict(f: Callable[..., object], **kwargs: object) -> object:
    """用 kwargs 调用 ``f``，把不接受的参数过滤掉。

    提示：f 接受 ``a, b, c``，但 kwargs 有 ``a, b, c, d``，只把 a, b, c 传进去。
    可以用 ``inspect.signature`` 检查参数名。
    """
    # TODO: 实现
    raise NotImplementedError


def merge(*dicts: dict[str, int]) -> dict[str, int]:
    """合并多个 dict，相同 key 累加 value。"""
    # TODO: 实现
    raise NotImplementedError


def apply_each(xs: list[int], *funcs: Callable[[int], int]) -> list[int]:
    """按顺序把 funcs 套在 xs 上。

    例：``apply_each([1, 2], lambda x: x + 1, lambda x: x * 2)`` -> ``[(1+1)*2, (2+1)*2]`` = ``[4, 6]``
    """
    # TODO: 实现
    raise NotImplementedError


def make_counter(start: int = 0) -> Callable[[], int]:
    """返回一个无参函数，每次调用返回递增的整数（从 start 开始）。"""
    # TODO: 实现
    raise NotImplementedError
