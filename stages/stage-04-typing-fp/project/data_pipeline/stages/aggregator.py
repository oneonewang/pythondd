"""Aggregator：把 EnrichRecord 列表聚合成 Summary。"""
from __future__ import annotations

from collections.abc import Iterable

from ..models import EnrichedRecord, Summary


class SummaryAggregator:
    """``Iterable[EnrichedRecord]`` -> :class:`Summary`：

    - ``total`` = 记录数
    - ``total_usd`` = 所有 amount_usd 之和
    - ``by_action`` = Counter(action)
    - ``by_category`` = Counter(category)
    """

    def aggregate(self, items: Iterable[EnrichedRecord]) -> Summary:
        # TODO
        raise NotImplementedError
