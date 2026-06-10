"""Analyzer 测试。"""
import pytest
from log_analyzer.analyzer import (
    count_by_level,
    find_anomalies,
    sliding_rate,
    take_errors,
)
from log_analyzer.models import LogRecord


def rec(ts: str, level: str, msg: str = "") -> LogRecord:
    return LogRecord(timestamp=ts, level=level, message=msg)


class TestCountByLevel:
    def test_basic(self) -> None:
        records = [
            rec("t1", "INFO"),
            rec("t2", "ERROR"),
            rec("t3", "INFO"),
            rec("t4", "WARN"),
        ]
        assert count_by_level(records) == {"INFO": 2, "ERROR": 1, "WARN": 1}

    def test_empty(self) -> None:
        assert count_by_level([]) == {}

    def test_works_with_generator(self) -> None:
        gen = (rec(str(i), "INFO") for i in range(100))
        assert count_by_level(gen) == {"INFO": 100}


class TestTakeErrors:
    def test_basic(self) -> None:
        records = [
            rec("t1", "INFO"),
            rec("t2", "ERROR", "first"),
            rec("t3", "INFO"),
            rec("t4", "ERROR", "second"),
            rec("t5", "ERROR", "third"),
        ]
        result = take_errors(records, 2)
        assert len(result) == 2
        assert [r.message for r in result] == ["first", "second"]

    def test_limit_larger_than_available(self) -> None:
        records = [rec("t1", "ERROR"), rec("t2", "ERROR")]
        assert len(take_errors(records, 10)) == 2

    def test_no_errors(self) -> None:
        records = [rec("t1", "INFO"), rec("t2", "WARN")]
        assert take_errors(records, 5) == []


class TestSlidingRate:
    def test_window_one(self) -> None:
        records = [rec("t1", "INFO"), rec("t2", "ERROR"), rec("t3", "ERROR")]
        rates = list(sliding_rate(records, window=1, level="ERROR"))
        assert len(rates) == 3
        assert rates[0].error_rate == 0.0
        assert rates[1].error_rate == 1.0
        assert rates[2].error_rate == 1.0

    def test_window_three(self) -> None:
        # 窗口需要填满才产出
        records = [
            rec("t1", "INFO"),
            rec("t2", "INFO"),
            rec("t3", "ERROR"),  # 窗口 [INFO, INFO, ERROR] -> 1/3
            rec("t4", "ERROR"),  # 窗口 [INFO, ERROR, ERROR] -> 2/3
            rec("t5", "INFO"),   # 窗口 [ERROR, ERROR, INFO] -> 2/3
        ]
        rates = list(sliding_rate(records, window=3, level="ERROR"))
        assert len(rates) == 3
        assert rates[0].error_rate == pytest.approx(1 / 3)
        assert rates[1].error_rate == pytest.approx(2 / 3)
        assert rates[2].error_rate == pytest.approx(2 / 3)

    def test_empty(self) -> None:
        assert list(sliding_rate([], window=5)) == []

    def test_line_no_increments(self) -> None:
        records = [rec(str(i), "INFO") for i in range(10)]
        rates = list(sliding_rate(records, window=3))
        assert [r.line_no for r in rates] == [3, 4, 5, 6, 7, 8, 9, 10]


class TestFindAnomalies:
    def test_filters_by_threshold(self) -> None:
        records = [
            rec("t1", "INFO"),
            rec("t2", "ERROR"),
            rec("t3", "ERROR"),
            rec("t4", "ERROR"),
            rec("t5", "INFO"),
        ]
        # window=2
        # 窗口 [INFO, ERROR] -> 1/2
        # 窗口 [ERROR, ERROR] -> 1
        # 窗口 [ERROR, INFO] -> 1/2
        anomalies = list(
            find_anomalies(records, window=2, threshold=0.5, level="ERROR")
        )
        assert len(anomalies) == 1
        assert anomalies[0].error_rate == 1.0

    def test_threshold_zero(self) -> None:
        records = [rec(str(i), "INFO") for i in range(5)]
        # 窗口 1：5 个产出，错误率全是 0
        anomalies = list(find_anomalies(records, window=1, threshold=0.0))
        assert anomalies == []

    def test_strict_greater_than(self) -> None:
        records = [rec("t1", "INFO"), rec("t2", "ERROR"), rec("t3", "INFO")]
        # window=3, [INFO, ERROR, INFO] -> 1/3，不超过 0.5
        anomalies = list(find_anomalies(records, window=3, threshold=0.5))
        assert anomalies == []
