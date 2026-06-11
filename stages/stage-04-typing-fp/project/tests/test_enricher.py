"""Enricher 测试。"""
import pytest
from data_pipeline.models import ValidatedRecord
from data_pipeline.stages.enricher import RecordEnricher


def make_validated(currency: str = "USD", action: str = "buy") -> ValidatedRecord:
    return ValidatedRecord(
        record_id="r1",
        user_id=1,
        timestamp="2024-01-15T10:00:00",   # Monday
        action=action,
        amount=100.0,
        currency=currency,
    )


class TestRecordEnricher:
    def test_usd_unchanged(self) -> None:
        e = RecordEnricher().enrich(make_validated("USD", "buy"))
        assert e.amount_usd == 100.0

    def test_eur_conversion(self) -> None:
        e = RecordEnricher().enrich(make_validated("EUR", "buy"))
        assert e.amount_usd == pytest.approx(108.0)

    def test_weekday_monday(self) -> None:
        e = RecordEnricher().enrich(make_validated("USD", "buy"))
        assert e.weekday == "Monday"

    def test_weekday_sunday(self) -> None:
        rec = make_validated().replace(timestamp="2024-01-21T10:00:00")
        e = RecordEnricher().enrich(rec)
        assert e.weekday == "Sunday"

    def test_category_trade(self) -> None:
        assert RecordEnricher().enrich(make_validated(action="buy")).category == "trade"
        assert RecordEnricher().enrich(make_validated(action="sell")).category == "trade"

    def test_category_funding(self) -> None:
        assert RecordEnricher().enrich(make_validated(action="deposit")).category == "funding"
        assert RecordEnricher().enrich(make_validated(action="withdraw")).category == "funding"
