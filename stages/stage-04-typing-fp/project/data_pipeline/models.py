"""所有 dataclass 模型（frozen=True）。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class ParsedRecord:
    """解析后的记录：原 dict 的"形状化"版本。"""

    record_id: str
    user_id: int
    timestamp: str        # ISO 8601
    action: str
    amount: float
    currency: str


@dataclass(frozen=True, slots=True)
class ValidatedRecord:
    """校验通过后的记录。"""

    record_id: str
    user_id: int
    timestamp: str
    action: str
    amount: float
    currency: str


@dataclass(frozen=True, slots=True)
class EnrichedRecord:
    """富化后的记录：带派生字段。"""

    record_id: str
    user_id: int
    timestamp: str
    action: str
    amount_usd: float      # 转换后
    weekday: str            # 派生自 timestamp
    category: str           # 由 action 派生


@dataclass(frozen=True, slots=True)
class Summary:
    """聚合统计。"""

    total: int
    total_usd: float
    by_action: dict[str, int]
    by_category: dict[str, int]


# 类型别名
Action = Literal["buy", "sell", "deposit", "withdraw"]
