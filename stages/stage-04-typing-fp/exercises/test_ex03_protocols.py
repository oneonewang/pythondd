"""Ex03 测试。"""

from .ex03_protocols import (
    ChainReader,
    StrBuffer,
    SupportsRead,
    SupportsReadWrite,
    SupportsWrite,
    total_length,
    write_all,
)


class TestStrBuffer:
    def test_read_write(self) -> None:
        b = StrBuffer("hello")
        assert b.read() == "hello"
        b.write(" world")
        assert b.read() == "hello world"

    def test_protocol_check(self) -> None:
        b = StrBuffer()
        assert isinstance(b, SupportsRead)
        assert isinstance(b, SupportsWrite)
        assert isinstance(b, SupportsReadWrite)

    def test_string_not_writable(self) -> None:
        assert not isinstance("x", SupportsWrite)


class TestTotalLength:
    def test_basic(self) -> None:
        streams = [StrBuffer("abc"), StrBuffer("hello"), StrBuffer("")]
        assert total_length(streams) == 8

    def test_empty(self) -> None:
        assert total_length([]) == 0


class TestWriteAll:
    def test_basic(self) -> None:
        streams = [StrBuffer(), StrBuffer()]
        n = write_all(streams, "data")
        assert n == 8
        for s in streams:
            assert s.read() == "data"


class TestChainReader:
    def test_concatenates(self) -> None:
        a = StrBuffer("hello ")
        b = StrBuffer("world")
        chain = ChainReader([a, b])
        assert chain.read() == "hello world"

    def test_empty(self) -> None:
        chain = ChainReader([])
        assert chain.read() == ""

    def test_is_readable(self) -> None:
        chain = ChainReader([StrBuffer("x")])
        assert isinstance(chain, SupportsRead)
