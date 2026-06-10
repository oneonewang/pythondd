"""Ex04 测试。"""
from pathlib import Path

import pytest

from .ex04_context_managers import Indenter, atomic_counter, swallow, temp_file


class TestIndenter:
    def test_basic(self, capsys) -> None:
        with Indenter() as ind:
            ind.print("a")
        captured = capsys.readouterr()
        assert captured.out == "a\n"

    def test_nested(self, capsys) -> None:
        with Indenter() as ind:
            ind.print("a")
            with ind:
                ind.print("b")
            ind.print("c")
        captured = capsys.readouterr()
        assert captured.out == "a\n  b\nc\n"

    def test_custom_indent(self, capsys) -> None:
        with Indenter(indent_unit="    ") as ind, ind:
            ind.print("x")
        captured = capsys.readouterr()
        assert captured.out == "    x\n"

    def test_restores_on_exception(self, capsys) -> None:
        ind = Indenter()
        with pytest.raises(ValueError), ind:
            raise ValueError()
        assert ind.level == 0


class TestTempFile:
    def test_creates_and_cleans_up(self) -> None:
        with temp_file("hello world", suffix=".log") as p:
            assert p.exists()
            assert p.read_text(encoding="utf-8") == "hello world"
            assert p.suffix == ".log"
        # 退出后被删除
        assert not p.exists()

    def test_returns_path(self) -> None:
        with temp_file("data") as p:
            assert isinstance(p, Path)


class TestSwallow:
    def test_swallows_matching(self, capsys) -> None:
        with swallow(ValueError, "caught one"):
            raise ValueError("boom")
        captured = capsys.readouterr()
        assert "caught one" in captured.out

    def test_propagates_other(self) -> None:
        with pytest.raises(RuntimeError), swallow(ValueError):
            raise RuntimeError("not caught")


class TestAtomicCounter:
    def test_no_exception_keeps_value(self) -> None:
        c = atomic_counter(0)
        with c:
            c.value += 1
        assert c.value == 1

    def test_exception_rolls_back(self) -> None:
        c = atomic_counter(5)
        with pytest.raises(RuntimeError), c:
            c.value = 100
            raise RuntimeError("abort")
        assert c.value == 5

    def test_nested_rollback(self) -> None:
        c = atomic_counter(10)
        with pytest.raises(ValueError), c:
            c.value = 20
            with c:
                c.value = 30
                raise ValueError("inner")
        assert c.value == 10
