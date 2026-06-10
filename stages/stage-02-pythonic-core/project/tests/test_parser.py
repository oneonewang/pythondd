"""Parser 测试。"""
from pathlib import Path

import pytest
from log_analyzer.parser import ParseStats, iter_lines, iter_records, parse_line

SAMPLE_LINES = [
    "2024-01-15T10:23:45 INFO User logged in user_id=1",
    "2024-01-15T10:23:46 ERROR Connection failed",
    "2024-01-15T10:23:47 WARN  Slow query",
    "bad line without enough fields",
    "2024-01-15T10:23:48 INFO another one",
]


@pytest.fixture
def log_file(tmp_path):
    p = tmp_path / "test.log"
    p.write_text("\n".join(SAMPLE_LINES) + "\n", encoding="utf-8")
    return p


class TestParseLine:
    def test_valid(self) -> None:
        rec = parse_line("2024-01-15T10:23:45 INFO hello world")
        assert rec.timestamp == "2024-01-15T10:23:45"
        assert rec.level == "INFO"
        assert rec.message == "hello world"

    def test_too_few_fields_raises(self) -> None:
        with pytest.raises(ValueError):
            parse_line("only one field")


class TestIterLines:
    def test_skips_empty(self, tmp_path) -> None:
        p = tmp_path / "x.log"
        p.write_text("a\n\nb\n\n", encoding="utf-8")
        assert list(iter_lines(p)) == ["a", "b"]

    def test_strips_crlf(self, tmp_path) -> None:
        p = tmp_path / "x.log"
        p.write_text("a\r\nb\r\n", encoding="utf-8")
        assert list(iter_lines(p)) == ["a", "b"]


class TestIterRecords:
    def test_basic(self, log_file) -> None:
        stats = ParseStats()
        records = list(iter_records(log_file, stats=stats))
        assert len(records) == 4
        assert records[0].level == "INFO"
        assert stats.parsed == 4
        assert stats.errors == 1

    def test_no_stats(self, log_file) -> None:
        records = list(iter_records(log_file))
        assert len(records) == 4

    def test_all_invalid(self, tmp_path) -> None:
        p = tmp_path / "bad.log"
        p.write_text("a\nb\nc\n", encoding="utf-8")
        stats = ParseStats()
        assert list(iter_records(p, stats=stats)) == []
        assert stats.errors == 3
        assert stats.total_lines == 3

    def test_is_generator(self) -> None:
        import types

        with pytest.raises((FileNotFoundError, OSError)):
            gen = iter_records(Path("/nonexistent"))
            assert isinstance(gen, types.GeneratorType)
