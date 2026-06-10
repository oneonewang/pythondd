"""Ex03 测试。"""
from .ex03_functions import apply_each, call_with_dict, make_counter, make_greeting, merge


class TestMakeGreeting:
    def test_default(self) -> None:
        greet = make_greeting()
        assert greet("Alice") == "Hello, Alice!"

    def test_custom(self) -> None:
        greet = make_greeting("Hi", "...")
        assert greet("Bob") == "Hi, Bob..."

    def test_partial(self) -> None:
        greet = make_greeting(punctuation="?")
        assert greet("Eve") == "Hello, Eve?"


class TestCallWithDict:
    def test_filter_extras(self) -> None:
        def f(a, b, c):
            return (a, b, c)

        assert call_with_dict(f, a=1, b=2, c=3, d=4) == (1, 2, 3)

    def test_no_extras(self) -> None:
        def f(x):
            return x * 2

        assert call_with_dict(f, x=5) == 10

    def test_missing_args_allowed(self) -> None:
        # 函数本身有默认参数时不应报错
        def f(a, b=10):
            return a + b

        assert call_with_dict(f, a=1) == 11


class TestMerge:
    def test_empty(self) -> None:
        assert merge() == {}

    def test_no_overlap(self) -> None:
        assert merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

    def test_overlap_sum(self) -> None:
        assert merge({"a": 1, "b": 2}, {"b": 3, "c": 4}) == {"a": 1, "b": 5, "c": 4}

    def test_three_dicts(self) -> None:
        assert merge({"x": 1}, {"x": 2}, {"x": 3}) == {"x": 6}


class TestApplyEach:
    def test_basic(self) -> None:
        result = apply_each([1, 2, 3], lambda x: x + 1, lambda x: x * 2)
        assert result == [4, 6, 8]

    def test_no_funcs(self) -> None:
        assert apply_each([1, 2, 3]) == [1, 2, 3]

    def test_single_func(self) -> None:
        assert apply_each([1, 2, 3], lambda x: -x) == [-1, -2, -3]


class TestMakeCounter:
    def test_default_start(self) -> None:
        c = make_counter()
        assert c() == 0
        assert c() == 1
        assert c() == 2

    def test_custom_start(self) -> None:
        c = make_counter(10)
        assert c() == 10
        assert c() == 11

    def test_independent_counters(self) -> None:
        c1 = make_counter()
        c2 = make_counter()
        c1()
        c1()
        assert c2() == 0
