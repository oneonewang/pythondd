"""Ex04 测试。"""
import pytest

from .ex04_abc_and_protocol import (
    Circle,
    FileLike,
    Rectangle,
    Shape,
    SupportsClose,
    SupportsRead,
    close_all,
    total_length,
)


class TestShape:
    def test_cannot_instantiate(self) -> None:
        with pytest.raises(TypeError):
            Shape()

    def test_rectangle(self) -> None:
        r = Rectangle(3, 4)
        assert r.area() == 12
        assert r.perimeter() == 14
        assert r.describe() == "Rectangle: area=12.00, perimeter=14.00"

    def test_circle(self) -> None:
        c = Circle(1)
        assert c.area() == pytest.approx(3.14159, rel=1e-3)
        assert c.perimeter() == pytest.approx(6.28318, rel=1e-3)

    def test_isinstance(self) -> None:
        assert isinstance(Rectangle(1, 1), Shape)
        assert isinstance(Circle(1), Shape)


class TestFileLike:
    def test_read(self) -> None:
        f = FileLike("hello")
        assert f.read() == "hello"
        assert not f.closed

    def test_close(self) -> None:
        f = FileLike("data")
        f.close()
        assert f.closed


class TestProtocolRuntime:
    def test_filelike_supports_both(self) -> None:
        f = FileLike("data")
        assert isinstance(f, SupportsRead)
        assert isinstance(f, SupportsClose)

    def test_plain_object_does_not(self) -> None:
        assert not isinstance("just a string", SupportsClose)
        assert not isinstance(42, SupportsRead)


class TestCloseAll:
    def test_closes_all(self) -> None:
        f1 = FileLike("a")
        f2 = FileLike("b")
        close_all([f1, f2])
        assert f1.closed
        assert f2.closed


class TestTotalLength:
    def test_sum_lengths(self) -> None:
        files = [FileLike("abc"), FileLike("hello")]
        assert total_length(files) == 8

    def test_empty(self) -> None:
        assert total_length([]) == 0
