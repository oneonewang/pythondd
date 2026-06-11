"""Ex01 测试。"""

from .ex01_typing_basics import (
    filter_by_level,
    make_user_id,
    parse_user,
    safe_first,
    user_label,
)


class TestParseUser:
    def test_valid(self) -> None:
        result = parse_user({"name": "alice", "age": 30, "email": "a@b.c"})
        assert result == {"name": "alice", "age": 30, "email": "a@b.c"}

    def test_missing_field(self) -> None:
        assert parse_user({"name": "alice", "age": 30}) is None

    def test_wrong_type(self) -> None:
        assert parse_user({"name": "alice", "age": "30", "email": "a@b.c"}) is None

    def test_empty(self) -> None:
        assert parse_user({}) is None


class TestFilterByLevel:
    def test_basic(self) -> None:
        records = [
            {"level": "INFO", "msg": "a"},
            {"level": "ERROR", "msg": "b"},
            {"level": "INFO", "msg": "c"},
            {"level": "WARN", "msg": "d"},
        ]
        result = filter_by_level(records, "INFO")
        assert len(result) == 2
        assert all(r["level"] == "INFO" for r in result)

    def test_no_match(self) -> None:
        records = [{"level": "INFO"}]
        assert filter_by_level(records, "ERROR") == []

    def test_empty(self) -> None:
        assert filter_by_level([], "INFO") == []


class TestUserId:
    def test_make_and_label(self) -> None:
        uid = make_user_id(42)
        assert user_label(uid, "alice") == "#42: alice"

    def test_id_is_int(self) -> None:
        assert isinstance(make_user_id(5), int)


class TestSafeFirst:
    def test_none(self) -> None:
        assert safe_first(None) is None

    def test_empty(self) -> None:
        assert safe_first([]) is None

    def test_value(self) -> None:
        assert safe_first([1, 2, 3]) == 1
