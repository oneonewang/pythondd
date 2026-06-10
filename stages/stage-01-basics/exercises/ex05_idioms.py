"""Ex05: 惯用法改写。

每题给你一份 non-pythonic 写法，请改写成 Pythonic 版本。函数签名保持不变。
"""
from __future__ import annotations

from collections.abc import Iterable


def total(nums: list[int]) -> int:
    """求和。

    Non-pythonic：手写累加。
    """
    # TODO: 改写为单行
    result = 0
    for n in nums:
        result = result + n
    return result


def find_evens(nums: list[int]) -> list[int]:
    """返回所有偶数。"""
    # TODO: 用列表推导式替换下面的循环
    result = []
    for n in nums:
        if n % 2 == 0:
            result.append(n)
    return result


def is_empty(collection) -> bool:
    """判断 collection 是否为空。"""
    # TODO: 用更 Pythonic 的写法
    if len(collection) == 0:
        return True
    else:
        return False


def first_n(items: list[str], n: int) -> list[str]:
    """返回前 n 个元素。n 超出列表长度时返回全部。"""
    # TODO: 用切片
    result = []
    for i in range(n):
        if i < len(items):
            result.append(items[i])
    return result


def has_positive(nums: Iterable[int]) -> bool:
    """判断是否包含正数。"""
    # TODO: 用 any()
    found = False
    for n in nums:
        if n > 0:
            found = True
            break
    return found


def count_upper(s: str) -> int:
    """统计大写字母数量。"""
    # TODO: 用 sum + 生成器
    count = 0
    for c in s:
        if c.isupper():
            count += 1
    return count


def build_index(pairs: Iterable[tuple[str, int]]) -> dict[str, list[int]]:
    """把 ``(key, value)`` 序列聚合成 ``{key: [value, ...]}``。"""
    # TODO: 用 setdefault 或 defaultdict
    result: dict[str, list[int]] = {}
    for k, v in pairs:
        if k not in result:
            result[k] = []
        result[k].append(v)
    return result


def swap_dict(d: dict[str, int]) -> dict[int, str]:
    """交换 key / value。值不唯一时取最后一个。"""
    # TODO: 用 dict 推导式
    result: dict[int, str] = {}
    for k, v in d.items():
        result[v] = k
    return result
