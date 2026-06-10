"""Ex02: 集合操作。

涵盖：list / tuple / set / dict 的选型、推导式、成员检查。
"""
from __future__ import annotations

from collections import Counter


def dedup_preserve_order(items: list[int]) -> list[int]:
    """去重并保持原顺序。

    例：``[3, 1, 3, 2, 1]`` -> ``[3, 1, 2]``

    要求：不要用 ``list(set(items))``，因为 set 不保序。
    """
    # TODO: 实现
    raise NotImplementedError


def group_by_first_letter(words: list[str]) -> dict[str, list[str]]:
    """按单词首字母（小写）分组。

    例：``["apple", "ant", "Banana"]`` -> ``{"a": ["apple", "ant"], "b": ["Banana"]}``

    提示：用 ``setdefault`` 或 ``defaultdict``。
    """
    # TODO: 实现
    raise NotImplementedError


def intersect_sorted(a: list[int], b: list[int]) -> list[int]:
    """返回两个**已排序**列表的交集，结果也排序去重。

    要求：O(n + m)，不要用 set。提示：双指针。
    """
    # TODO: 实现
    raise NotImplementedError


def top_n_frequent(items: list[str], n: int) -> list[tuple[str, int]]:
    """返回出现频率最高的 ``n`` 个 (item, count)，按 count 降序、count 相同时按 item 升序。

    提示：用 ``collections.Counter`` 的 ``most_common``。
    """
    # TODO: 实现
    raise NotImplementedError


def chunk(items: list[int], size: int) -> list[list[int]]:
    """把列表切成 ``size`` 大小的块，最后一块可能更短。

    例：``chunk([1,2,3,4,5], 2)`` -> ``[[1,2],[3,4],[5]]``

    要求：自己实现，练习切片与推导式。
    """
    # TODO: 实现
    raise NotImplementedError
