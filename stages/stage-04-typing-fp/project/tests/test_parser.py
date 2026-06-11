"""Parser 测试。"""
import pytest
from data_pipeline.stages.parser import DictParser

RAW_OK = {
    "record_id": "r1",
    "user_id": 1,
    "timestamp": "2024-01-15T10:00:00",
    "action": "buy",
    "amount": 100.0,
    "currency": "USD",
}


class TestDictParser:
    def test_valid(self) -> None:
        rec = DictParser().parse(RAW_OK)
        assert rec.record_id == "r1"
        assert rec.amount == 100.0
        assert rec.currency == "USD"

    def test_missing_field(self) -> None:
        bad = {k: v for k, v in RAW_OK.items() if k != "amount"}
        with pytest.raises(ValueError):
            DictParser().parse(bad)

    def test_wrong_type(self) -> None:
        bad = dict(RAW_OK, user_id="not an int")
        with pytest.raises((ValueError, TypeError)):
            DictParser().parse(bad)
