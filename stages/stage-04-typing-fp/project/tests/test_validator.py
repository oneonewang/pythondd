"""Validator 测试。"""

from data_pipeline.models import ParsedRecord
from data_pipeline.stages.validator import RecordValidator


def make(record_id="r1", user_id=1, action="buy", amount=10.0, currency="USD") -> ParsedRecord:
    return ParsedRecord(
        record_id=record_id,
        user_id=user_id,
        timestamp="2024-01-15T10:00:00",
        action=action,
        amount=amount,
        currency=currency,
    )


class TestRecordValidator:
    def test_valid(self) -> None:
        v = RecordValidator().validate(make())
        assert v is not None
        assert v.record_id == "r1"

    def test_negative_amount(self) -> None:
        assert RecordValidator().validate(make(amount=-1)) is None

    def test_zero_amount(self) -> None:
        assert RecordValidator().validate(make(amount=0)) is None

    def test_bad_action(self) -> None:
        assert RecordValidator().validate(make(action="hack")) is None

    def test_bad_currency(self) -> None:
        assert RecordValidator().validate(make(currency="XXX")) is None
