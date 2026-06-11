"""Pipeline：把多阶段串起来。"""
from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

from .protocols import Aggregator, Enricher, Validator

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
W = TypeVar("W")


@dataclass
class Pipeline(Generic[T, U]):
    """单一转换管线：``T -> U``。

    支持 ``|`` 串联：``p1 | p2`` 得到 :class:`ChainedPipeline`。
    """

    transformer: object                                # Transformer[T, U]

    def run(self, data: T) -> U:
        # TODO: 调用 transformer.transform(data)
        raise NotImplementedError

    def __or__(self, other: object) -> ChainedPipeline[T, U]:
        return ChainedPipeline(stages=[self.transformer, other])


@dataclass
class ChainedPipeline(Generic[T, U]):
    """串联多条管线：``T -> ... -> W``。"""

    stages: list[object]

    def run(self, data: object) -> object:
        # TODO: 依次跑每一阶段
        raise NotImplementedError
