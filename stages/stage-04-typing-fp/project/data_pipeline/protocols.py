"""抽象协议：所有阶段都通过协议解耦。"""
from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol, TypeVar

# 注：Protocol 自身是不变的（invariant），所以 T/U 用默认的不变 TypeVar
T = TypeVar("T")
U = TypeVar("U")


class Transformer(Protocol[T, U]):
    """通用转换器。"""

    def transform(self, x: T) -> U: ...


class Validator(Protocol[T]):
    """校验器：返回 ``T`` 或 ``None``（None 表示失败）。"""

    def validate(self, x: T) -> T | None: ...


class Enricher(Protocol[T, U]):
    """富化器：给 ``T`` 加上派生字段得到 ``U``。"""

    def enrich(self, x: T) -> U: ...


class Aggregator(Protocol[T, U]):
    """聚合器：把可迭代的 ``T`` 聚合成 ``U``。"""

    def aggregate(self, items: Iterable[T]) -> U: ...
