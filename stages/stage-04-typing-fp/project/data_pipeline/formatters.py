"""按类型分派的格式化器。"""
from __future__ import annotations

from functools import singledispatch


@singledispatch
def format_value(value) -> str:
    """按类型分派格式化。

    - ``int`` -> ``"42"``
    - ``float`` -> ``"3.14"`` 保留 2 位
    - ``str`` -> ``'\"hi\"'``
    - ``list`` -> ``"[1, 2, 3]"`` 递归
    - ``dict`` -> ``"{a: 1, b: 2}"``
    - ``None`` -> ``"null"``
    """
    # TODO
    raise NotImplementedError


# TODO: 给 format_value 注册 int / float / str / list / dict / None
