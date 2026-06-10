"""Storage 层测试。"""
import json

import pytest
from todo_cli import storage
from todo_cli.storage import StorageError


def make_todo(todo_id: int, title: str) -> dict:
    return {
        "id": todo_id,
        "title": title,
        "done": False,
        "created_at": "2024-01-01T00:00:00+00:00",
    }


class TestLoad:
    def test_missing_file_returns_empty(self, tmp_path) -> None:
        path = tmp_path / "missing.json"
        assert storage.load_todos(path) == []

    def test_existing_file(self, tmp_path) -> None:
        path = tmp_path / "todos.json"
        path.write_text(json.dumps([make_todo(1, "a")]), encoding="utf-8")
        result = storage.load_todos(path)
        assert len(result) == 1
        assert result[0]["title"] == "a"

    def test_invalid_json_raises(self, tmp_path) -> None:
        path = tmp_path / "bad.json"
        path.write_text("not json", encoding="utf-8")
        with pytest.raises(StorageError):
            storage.load_todos(path)


class TestSave:
    def test_roundtrip(self, tmp_path) -> None:
        path = tmp_path / "out.json"
        todos = [make_todo(1, "a"), make_todo(2, "b")]
        storage.save_todos(path, todos)
        assert storage.load_todos(path) == todos

    def test_creates_parent_dirs(self, tmp_path) -> None:
        path = tmp_path / "a" / "b" / "todos.json"
        storage.save_todos(path, [make_todo(1, "x")])
        assert path.exists()

    def test_overwrites(self, tmp_path) -> None:
        path = tmp_path / "todos.json"
        storage.save_todos(path, [make_todo(1, "first")])
        storage.save_todos(path, [make_todo(2, "second")])
        result = storage.load_todos(path)
        assert len(result) == 1
        assert result[0]["id"] == 2
