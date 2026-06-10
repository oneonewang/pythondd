"""Service 层测试。"""
import pytest
from todo_cli import service
from todo_cli.service import TodoNotFoundError


def make_todo(todo_id: int, title: str, done: bool = False) -> dict:
    return {
        "id": todo_id,
        "title": title,
        "done": done,
        "created_at": "2024-01-01T00:00:00+00:00",
    }


class TestAdd:
    def test_first_todo_id_starts_at_1(self) -> None:
        todos: list[dict] = []
        t = service.add(todos, "first")
        assert t["id"] == 1
        assert t["title"] == "first"
        assert t["done"] is False
        assert "created_at" in t
        assert todos == [t]

    def test_subsequent_ids_increment(self) -> None:
        todos: list[dict] = []
        service.add(todos, "a")
        service.add(todos, "b")
        service.add(todos, "c")
        assert [t["id"] for t in todos] == [1, 2, 3]

    def test_ids_continue_from_existing_max(self) -> None:
        todos = [make_todo(5, "old")]
        t = service.add(todos, "new")
        assert t["id"] == 6


class TestListTodos:
    def test_undone_first(self) -> None:
        todos = [
            make_todo(1, "done one", done=True),
            make_todo(2, "undone"),
            make_todo(3, "done two", done=True),
            make_todo(4, "also undone"),
        ]
        result = service.list_todos(todos)
        assert [t["id"] for t in result] == [2, 4, 1, 3]

    def test_include_done_false(self) -> None:
        todos = [
            make_todo(1, "done one", done=True),
            make_todo(2, "undone"),
        ]
        result = service.list_todos(todos, include_done=False)
        assert [t["id"] for t in result] == [2]

    def test_empty(self) -> None:
        assert service.list_todos([]) == []


class TestComplete:
    def test_marks_done(self) -> None:
        todos = [make_todo(1, "task")]
        result = service.complete(todos, 1)
        assert result["done"] is True
        assert todos[0]["done"] is True

    def test_idempotent(self) -> None:
        todos = [make_todo(1, "task")]
        service.complete(todos, 1)
        result = service.complete(todos, 1)
        assert result["done"] is True

    def test_not_found(self) -> None:
        todos = [make_todo(1, "task")]
        with pytest.raises(TodoNotFoundError):
            service.complete(todos, 99)


class TestRemove:
    def test_removes(self) -> None:
        todos = [make_todo(1, "a"), make_todo(2, "b")]
        result = service.remove(todos, 1)
        assert result["title"] == "a"
        assert [t["id"] for t in todos] == [2]

    def test_not_found(self) -> None:
        todos = [make_todo(1, "a")]
        with pytest.raises(TodoNotFoundError):
            service.remove(todos, 99)


class TestClearDone:
    def test_returns_count(self) -> None:
        todos = [
            make_todo(1, "a", done=True),
            make_todo(2, "b"),
            make_todo(3, "c", done=True),
        ]
        n = service.clear_done(todos)
        assert n == 2
        assert [t["id"] for t in todos] == [2]

    def test_no_done(self) -> None:
        todos = [make_todo(1, "a"), make_todo(2, "b")]
        assert service.clear_done(todos) == 0
        assert len(todos) == 2
