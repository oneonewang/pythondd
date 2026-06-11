"""Ex01: GIL 与 threading。

涵盖：``threading.Thread``、``ThreadPoolExecutor``、IO 密集并行。
"""
from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any


def run_io_tasks(tasks: list[Any], max_workers: int = 4) -> list[Any]:
    """并发跑 IO 任务（用 ``time.sleep`` 模拟）。

    每个任务 ``t`` 是 ``(duration, result)``：sleep ``duration`` 秒后返回 ``result``。
    4 个 0.1s 任务并发应该 ≈ 0.1s（不是 0.4s）。
    """
    # TODO: 用 ThreadPoolExecutor 实现
    raise NotImplementedError


def run_serial(tasks: list[Any]) -> list[Any]:
    """串行跑同一组任务（用于对比）。"""
    # TODO
    raise NotImplementedError


def parallel_speedup(tasks: list[Any], max_workers: int = 4) -> float:
    """返回 ``run_serial / run_io_tasks`` 的加速比（speedup）。

    例：``parallel_speedup([(0.1, 1)] * 4)`` 应接近 4.0
    """
    # TODO
    raise NotImplementedError


def counter_unsafe(n_threads: int = 10, increments: int = 100_000) -> int:
    """演示竞态：返回不正确的 counter 值（用于对比）。"""
    counter = 0

    def inc() -> None:
        nonlocal counter
        for _ in range(increments):
            counter += 1

    threads = [threading.Thread(target=inc) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return counter


def counter_with_lock(n_threads: int = 10, increments: int = 100_000) -> int:
    """用 ``threading.Lock`` 修复，返回正确值。"""
    # TODO
    raise NotImplementedError


class ThreadLocalStorage:
    """每个线程独立的存储。"""

    def __init__(self) -> None:
        # TODO: 用 threading.local
        ...

    def set(self, value: Any) -> None:
        # TODO
        ...

    def get(self) -> Any:
        # TODO
        raise NotImplementedError
