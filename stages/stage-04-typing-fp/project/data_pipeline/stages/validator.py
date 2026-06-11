"""Validator：检查 ParsedRecord 字段是否合法。"""
from __future__ import annotations

from ..models import ParsedRecord, ValidatedRecord

ALLOWED_ACTIONS = frozenset({"buy", "sell", "deposit", "withdraw"})
ALLOWED_CURRENCIES = frozenset({"USD", "EUR", "JPY", "CNY", "GBP"})


class RecordValidator:
    """校验 :class:`ParsedRecord` -> :class:`ValidatedRecord` 或 None。"""

    def validate(self, record: ParsedRecord) -> ValidatedRecord | None:
        # TODO: 校验 amount > 0、action 合法、currency 合法
        raise NotImplementedError
