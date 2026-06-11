"""自定义错误。"""
from __future__ import annotations


class PipelineError(Exception):
    """管线层错误基类。"""


class ValidationError(PipelineError):
    """记录校验失败。"""

    def __init__(self, record_id: str, message: str) -> None:
        super().__init__(f"[{record_id}] {message}")
        self.record_id = record_id
        self.message = message
