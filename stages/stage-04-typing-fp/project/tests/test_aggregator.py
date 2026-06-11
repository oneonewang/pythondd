"""Aggregator 测试。"""

from data_pipeline.models import EnrichedRecord
from data_pipeline.stages.aggregator import SummaryAggregator


def rec(record_id: str, action: str, category: str, amount_usd: float) -> EnrichedRecord:
    return EnrichedRecord(
        record_id=record_id,
        user_id=1,
        timestamp="2024-01-15T10:00:00",
        action=action,
        amount_usd=amount_usd,
        weekday="Monday",
        category=category,
    )


class TestSummaryAggregator:
    def test_empty(self) -> None:
        s = SummaryAggregator().aggregate([])
        assert s.total == 0
        assert s.total_usd == 0.0
        assert s.by_action == {}
        assert s.by_category == {}

    def test_basic(self) -> None:
        records = [
            rec("a", "buy", "trade", 100.0),
            rec("b", "sell", "trade", 50.0),
            rec("c", "deposit", "funding", 200.0),
        ]
        s = SummaryAggregator().aggregate(records)
        assert s.total == 3
        assert s.total_usd == 350.0
        assert s.by_action == {"buy": 1, "sell": 1, "deposit": 1}
        assert s.by_category == {"trade": 2, "funding": 1}

    def test_accepts_generator(self) -> None:
        gen = (rec("a", "buy", "trade", 100.0) for _ in range(3))
        s = SummaryAggregator().aggregate(gen)
        assert s.total == 3
