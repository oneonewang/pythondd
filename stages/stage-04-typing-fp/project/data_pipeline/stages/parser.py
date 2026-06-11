"""Parser：把 dict 解析成 ParsedRecord。"""
from __future__ import annotations

from ..models import ParsedRecord


class DictParser:
    """把 ``dict`` 解析成 :class:`ParsedRecord`。

    字段要求：
    - record_id: str
    - user_id: int
    - timestamp: str
    - action: str
    - amount: float
    - currency: str

    缺字段或类型不符抛 :class:`ValueError`。
    """

    REQUIRED = ("record_id", "user_id", "timestamp", "action", "amount", "currency")

    def parse(self, raw: dict) -> ParsedRecord:
        # TODO: 实现
        raise NotImplementedError
