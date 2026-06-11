"""Ex01 测试。"""

from .ex01_classes_and_mro import D, diamond_super_chain, mro_chain, singleton


class TestMRO:
    def test_mro_chain(self) -> None:
        assert mro_chain(D) == "D -> B -> C -> A -> object"

    def test_diamond_init_order(self) -> None:
        # A/B/C/D 都用 super().__init__() 协作，链是 D → B → C → A
        assert diamond_super_chain(D) == ["D", "B", "C", "A"]


class TestSingleton:
    def test_returns_same_instance(self) -> None:
        @singleton
        class C:
            def __init__(self, x):
                self.x = x

        a = C(1)
        b = C(2)
        assert a is b
        assert a.x == 1            # 第一次构造的值；第二次参数被忽略

    def test_preserves_class(self) -> None:
        @singleton
        class C:
            pass

        assert isinstance(C(), C)
