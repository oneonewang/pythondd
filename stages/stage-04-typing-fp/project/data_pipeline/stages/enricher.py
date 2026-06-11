"""Enricher：给 ValidatedRecord 加上派生字段。"""
from __future__ import annotations

from ..models import EnrichedRecord, ValidatedRecord

# 货币 -> USD 汇率（写死示例）
RATES = {
    "USD": 1.0,
    "EUR": 1.08,
    "JPY": 0.0067,
    "CNY": 0.14,
    "GBP": 1.27,
}

# action -> category
CATEGORIES = {
    "buy": "trade",
    "sell": "trade",
    "deposit": "funding",
    "withdraw": "funding",
}


class RecordEnricher:
    """``ValidatedRecord`` -> :class:`EnrichedRecord`：

    - 派生 ``amount_usd = amount * rate[currency]``
    - 派生 ``weekday`` from ``timestamp``（周一 ~ 周日）
    - 派生 ``category`` from ``action``
    """

    def enrich(self, record: ValidatedRecord) -> EnrichedRecord:
        # TODO
        raise NotImplementedError
