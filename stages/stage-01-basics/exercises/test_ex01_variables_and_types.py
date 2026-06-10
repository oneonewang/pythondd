"""Ex01 测试。"""
import pytest

from .ex01_variables_and_types import format_person, is_palindrome, repeat, safe_int


class TestFormatPerson:
    def test_basic(self) -> None:
        assert format_person("Alice", 30, 1.68) == "Alice (30) - 1.68m"

    def test_height_two_decimals(self) -> None:
        assert format_person("Bob", 25, 1.7) == "Bob (25) - 1.70m"

    def test_zero_height(self) -> None:
        assert format_person("Carol", 0, 0) == "Carol (0) - 0.00m"


class TestIsPalindrome:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("Aba", True),
            ("  Race car  ", True),
            ("hello", False),
            ("", True),
            ("a", True),
            ("ab", False),
            ("12321", True),
        ],
    )
    def test_cases(self, text: str, expected: bool) -> None:
        assert is_palindrome(text) is expected


class TestSafeInt:
    def test_valid(self) -> None:
        assert safe_int("42") == 42

    def test_invalid_returns_default(self) -> None:
        assert safe_int("not a number") == 0
        assert safe_int("not a number", -1) == -1

    def test_negative(self) -> None:
        assert safe_int("-5") == -5


class TestRepeat:
    def test_zero(self) -> None:
        assert repeat("ab", 0) == ""

    def test_one(self) -> None:
        assert repeat("x", 1) == "x"

    def test_many(self) -> None:
        assert repeat("ab", 3) == "ababab"
