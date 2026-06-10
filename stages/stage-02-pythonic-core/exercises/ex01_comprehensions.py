"""Ex01: 推导式。

涵盖：list/dict/set 推导式、嵌套、生成器表达式、walrus。
"""
from __future__ import annotations


def matrix_flatten(matrix: list[list[int]]) -> list[int]:
    """把二维 list 展平成一维 list。

    例：``[[1, 2], [3, 4]]`` -> ``[1, 2, 3, 4]``

    要求：list 推导式。
    """
    # TODO: 实现
    raise NotImplementedError


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """转置方阵。

    例：``[[1, 2, 3], [4, 5, 6], [7, 8, 9]]`` -> ``[[1, 4, 7], [2, 5, 8], [3, 6, 9]]``

    要求：嵌套 list 推导式。
    """
    # TODO: 实现
    raise NotImplementedError


def word_lengths(words: list[str]) -> dict[str, int]:
    """``{word: len(word)}``，但只保留长度 >= 3 的词。"""
    # TODO: dict 推导式
    raise NotImplementedError


def unique_lengths(words: list[str]) -> set[int]:
    """返回所有不同长度的集合。"""
    # TODO: set 推导式
    raise NotImplementedError


def first_n_squares(n: int) -> list[int]:
    """返回前 n 个平方数。要求用生成器表达式（``sum``/``list`` 包一下）。"""
    # TODO: 实现
    raise NotImplementedError


def cartesian_product(xs: list[int], ys: list[int]) -> list[tuple[int, int]]:
    """返回 xs × ys 的笛卡尔积（顺序：先 y 后 x）。"""
    # TODO: 实现
    raise NotImplementedError


def index_above_threshold(xs: list[int], threshold: int) -> dict[int, int]:
    """返回 ``{value: index}``，只包含 ``value > threshold`` 的项。"""
    # TODO: 用 enumerate
    raise NotImplementedError


def pair_with_index(words: list[str]) -> list[tuple[int, str]]:
    """``[(0, words[0]), (1, words[1]), ...]``"""
    # TODO: enumerate + 推导式
    raise NotImplementedError
