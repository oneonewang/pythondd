"""Pipeline 端到端测试。"""

import pytest
from data_pipeline.formatters import format_value
from data_pipeline.stages.aggregator import SummaryAggregator
from data_pipeline.stages.enricher import RecordEnricher
from data_pipeline.stages.parser import DictParser
from data_pipeline.stages.validator import RecordValidator

SAMPLE_RAW = [
    {
        "record_id": "r1",
        "user_id": 1,
        "timestamp": "2024-01-15T10:00:00",
        "action": "buy",
        "amount": 100.0,
        "currency": "USD",
    },
    {
        "record_id": "r2",
        "user_id": 1,
        "timestamp": "2024-01-15T10:00:01",
        "action": "sell",
        "amount": 50.0,
        "currency": "EUR",
    },
    {
        "record_id": "r3",
        "user_id": 2,
        "timestamp": "2024-01-15T10:00:02",
        "action": "deposit",
        "amount": -10.0,    # 无效
        "currency": "USD",
    },
    {
        # 缺 amount
        "record_id": "r4",
        "user_id": 2,
        "timestamp": "2024-01-15T10:00:03",
        "action": "withdraw",
        "currency": "GBP",
    },
]


class TestEndToEnd:
    def test_full_pipeline(self) -> None:
        parser_ = DictParser()
        validator = RecordValidator()
        enricher = RecordEnricher()

        valid: list = []
        for raw in SAMPLE_RAW:
            try:
                p = parser_.parse(raw)
            except (ValueError, KeyError, TypeError):
                continue
            v = validator.validate(p)
            if v is not None:
                valid.append(v)

        enriched = [enricher.enrich(v) for v in valid]
        summary = SummaryAggregator().aggregate(enriched)

        assert summary.total == 2
        assert summary.total_usd == pytest.approx(100 + 54, rel=1e-2)  # USD 100 + EUR 50 * 1.08
        assert summary.by_category == {"trade": 2}


class TestFormatters:
    def test_int(self) -> None:
        assert format_value(42) == "42"

    def test_float(self) -> None:
        assert format_value(3.14159) == "3.14"

    def test_str(self) -> None:
        assert format_value("hi") == '"hi"'

    def test_list(self) -> None:
        assert format_value([1, 2, 3]) == "[1, 2, 3]"

    def test_dict(self) -> None:
        result = format_value({"a": 1, "b": 2})
        # dict 顺序无关紧要
        assert "a: 1" in result and "b: 2" in result

    def test_none(self) -> None:
        assert format_value(None) == "null"

    def test_unsupported_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            format_value({1, 2})
