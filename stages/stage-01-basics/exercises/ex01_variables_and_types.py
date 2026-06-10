"""Ex01: 变量、类型、字符串。

涵盖：动态类型、字符串格式化、字符串方法、不可变性。
"""
from __future__ import annotations


def format_person(name: str, age: int, height_m: float) -> str:
    """返回形如 ``"Alice (30) - 1.68m"`` 的字符串。

    要求：
    - 使用 f-string
    - 身高保留两位小数
    - name 原样输出（不要做大小写转换）
    """
    # TODO: 实现
    raise NotImplementedError


def is_palindrome(s: str) -> bool:
    """判断 ``s`` 是否回文（忽略大小写、忽略首尾空白）。

    例如：
    - ``"Aba"`` -> True
    - ``"  Race car  "`` -> True
    - ``"hello"`` -> False

    提示：先 ``s.strip().lower()`` 再比较。
    """
    # TODO: 实现
    raise NotImplementedError


def safe_int(s: str, default: int = 0) -> int:
    """把字符串转成 int，失败时返回 ``default``（不抛异常）。"""
    # TODO: 实现
    raise NotImplementedError


def repeat(s: str, n: int) -> str:
    """返回 ``s`` 重复 ``n`` 次的结果。

    要求：自己实现（不要用 ``s * n``），以便练习字符串拼接。
    """
    # TODO: 实现
    raise NotImplementedError
