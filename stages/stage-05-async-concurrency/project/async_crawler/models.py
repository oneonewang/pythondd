"""数据模型。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FetchResult:
    """一次 fetch 的结果。"""

    url: str
    status: int                       # HTTP 状态码；失败时 = 0
    content: str                      # 响应内容（截断到 max_bytes）
    error: str | None = None          # 失败原因
    duration_ms: float = 0.0          # 耗时（毫秒）

    @property
    def ok(self) -> bool:
        return self.error is None and 200 <= self.status < 300
