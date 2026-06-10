"""Ex04 测试。"""
import json

import pytest

from .ex04_io_and_exceptions import (
    StorageError,
    read_json_safely,
    read_lines_stripped,
    safe_div,
    write_csv,
    write_json,
)


class TestReadJsonSafely:
    def test_missing_file_returns_default(self, tmp_path) -> None:
        path = tmp_path / "missing.json"
        assert read_json_safely(path, default={"x": 1}) == {"x": 1}
        assert read_json_safely(path) is None

    def test_valid_file(self, tmp_path) -> None:
        path = tmp_path / "data.json"
        path.write_text(json.dumps({"a": 1}), encoding="utf-8")
        assert read_json_safely(path) == {"a": 1}

    def test_invalid_json_raises(self, tmp_path) -> None:
        path = tmp_path / "bad.json"
        path.write_text("not json", encoding="utf-8")
        with pytest.raises(StorageError):
            read_json_safely(path)


class TestWriteJson:
    def test_roundtrip(self, tmp_path) -> None:
        path = tmp_path / "nested" / "data.json"
        data = {"name": "你好", "list": [1, 2, 3]}
        write_json(path, data)
        assert read_json_safely(path) == data

    def test_creates_parent_dirs(self, tmp_path) -> None:
        path = tmp_path / "a" / "b" / "c.json"
        write_json(path, {})
        assert path.exists()


class TestWriteCsv:
    def test_basic(self, tmp_path) -> None:
        path = tmp_path / "out.csv"
        rows = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        write_csv(path, rows, ["name", "age"])
        text = path.read_text(encoding="utf-8")
        assert "name,age" in text
        assert "Alice,30" in text
        assert "Bob,25" in text


class TestReadLinesStripped:
    def test_basic(self, tmp_path) -> None:
        path = tmp_path / "f.txt"
        path.write_text("  a  \n\n  b  \n   \n", encoding="utf-8")
        assert read_lines_stripped(path) == ["a", "b"]

    def test_empty_file(self, tmp_path) -> None:
        path = tmp_path / "empty.txt"
        path.write_text("", encoding="utf-8")
        assert read_lines_stripped(path) == []


class TestSafeDiv:
    def test_normal(self) -> None:
        assert safe_div(10, 2) == 5.0

    def test_zero(self) -> None:
        assert safe_div(1, 0) == "inf"
