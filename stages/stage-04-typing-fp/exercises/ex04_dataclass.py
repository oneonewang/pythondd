"""Ex04: dataclass。

涵盖：``frozen``、``slots``、``__post_init__``、``field(default_factory=...)``、``replace``、``order``、``KW_ONLY``。
"""
from __future__ import annotations

from dataclasses import KW_ONLY, dataclass, field, replace
from datetime import date


@dataclass(frozen=True, slots=True)
class Money:
    """带币种的金额。"""

    amount: float
    currency: str
    _: KW_ONLY
    as_of: date | None = None

    def __post_init__(self) -> None:
        # TODO: 校验 amount >= 0、currency 长度 3
        ...


@dataclass(frozen=True)
class Version:
    """语义化版本。"""

    major: int
    minor: int
    patch: int

    def __post_init__(self) -> None:
        # TODO: 校验 major/minor/patch >= 0
        ...

    @classmethod
    def parse(cls, s: str) -> Version:
        # TODO: 解析 "1.2.3" -> Version(1, 2, 3)
        raise NotImplementedError

    def bump_major(self) -> Version:
        # TODO
        raise NotImplementedError


@dataclass(order=True)
class Task:
    """带优先级的任务，可排序。"""

    priority: int
    title: str = field(compare=False)
    tags: list[str] = field(default_factory=list, compare=False)
    _id: int = field(init=False, compare=False, default=0)

    def __post_init__(self) -> None:
        # TODO: 派生 _id
        ...


@dataclass
class Counter:
    """可变计数器。"""

    initial: int = 0
    _value: int = field(init=False)

    def __post_init__(self) -> None:
        # TODO
        ...

    def inc(self, n: int = 1) -> None:
        # TODO
        ...

    def dec(self, n: int = 1) -> None:
        # TODO
        ...

    @property
    def value(self) -> int:
        # TODO
        ...
