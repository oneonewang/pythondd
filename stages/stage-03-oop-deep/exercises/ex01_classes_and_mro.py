"""Ex01: 类基础与 MRO。

涵盖：``__init__`` / ``__new__``、``super()``、C3 线性化。
"""
from __future__ import annotations


class A:
    """顶级基类。"""

    def __init__(self) -> None:
        # TODO: 打印 "A.__init__"，调用 super().__init__()
        ...


class B(A):
    def __init__(self) -> None:
        # TODO: 打印 "B.__init__"，调用 super()
        ...


class C(A):
    def __init__(self) -> None:
        # TODO: 打印 "C.__init__"，调用 super()
        ...


class D(B, C):
    def __init__(self) -> None:
        # TODO: 打印 "D.__init__"，调用 super()
        ...


def singleton(cls):
    """类装饰器：把 ``cls`` 变成单例（重复构造返回同一实例）。

    用 ``__new__`` 实现。
    """
    # TODO: 实现
    raise NotImplementedError


def mro_chain(cls: type) -> str:
    """返回 ``cls.__mro__`` 中类名拼接的 " -> " 字符串。

    例：``MRO[D]`` -> ``"D -> B -> C -> A -> object"``
    """
    # TODO: 实现
    raise NotImplementedError


def diamond_super_chain(cls: type) -> list[str]:
    """协作式 ``__init__``：返回 ``cls()`` 时按 MRO 顺序触发的 ``__init__`` 名。

    通过让所有基类都调 ``super().__init__()``，可以遍历菱形。

    返回形如 ``["D", "B", "C", "A"]``。
    """
    # TODO: 借助 monkey patching 或重新定义类来观察
    raise NotImplementedError
