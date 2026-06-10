"""Ex05: 魔术方法。

目标：让自定义类型用起来像内置集合/字符串。
"""
from __future__ import annotations

from collections.abc import Iterator


class Bag[T]:
    """一个不可变的多重集合。

    - 构造：``Bag([1, 1, 2, 3])``
    - ``len(b)``：元素总数（含重复）
    - ``b.count(x)``：x 出现次数
    - ``b[x]``：返回 x 的计数（不存在为 0）
    - ``x in b``：x 至少出现一次
    - ``for x in b``：按出现次数重复产出元素（``[1, 1, 2, 3]``）
    - ``b == other``：按 ``Counter`` 比较
    - ``repr(b)``：``Bag([1, 1, 2, 3])``
    """

    def __init__(self, items: list[T]) -> None:
        # TODO: 保存 items（不复制要求，phase 4 会换 dataclass）
        ...

    # TODO: 实现以下魔术方法
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[T]: ...
    def __contains__(self, item: object) -> bool: ...
    def __getitem__(self, key: T) -> int: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...      # 让 Bag 可哈希（不变量：等于则 hash 等）
    def __repr__(self) -> str: ...
    def __bool__(self) -> bool: ...

    def count(self, item: T) -> int:
        # TODO: 计数
        ...


class Money:
    """带币种的金额。

    - 构造：``Money(10, "USD")``
    - ``__add__``：同币种可加，不同币种抛 ``ValueError``
    - ``__mul__``：支持 int/float 标量乘
    - ``__eq__``：币种 + 金额都等
    - ``__lt__``：同币种比金额，否则 ``NotImplemented``
    - ``__repr__``：``"10.00 USD"``
    """

    def __init__(self, amount: float, currency: str) -> None:
        # TODO
        ...

    def __add__(self, other: Money) -> Money:
        # TODO
        ...

    def __mul__(self, factor: float) -> Money:
        # TODO
        ...

    def __eq__(self, other: object) -> bool:
        # TODO
        ...

    def __lt__(self, other: Money) -> bool:
        # TODO
        ...

    def __hash__(self) -> int:
        # TODO
        ...

    def __repr__(self) -> str:
        # TODO
        ...


class Repeater:
    """调用次数计数器。

    - 构造：``Repeater()`` 初始 0
    - 每次 ``r()`` 返回当前计数（从 0 开始自增）
    - ``len(r)`` 返回调用次数
    - ``repr(r)``：``"Repeater(n=3)"``
    """

    def __init__(self) -> None:
        # TODO
        ...

    def __call__(self) -> int:
        # TODO
        ...

    def __len__(self) -> int:
        # TODO
        ...

    def __repr__(self) -> str:
        # TODO
        ...
