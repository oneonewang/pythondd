# 01 - 类基础与 MRO

## 1.1 类与实例

```python
class Point:
    """Point 类的 docstring。"""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

p = Point(1, 2)
```

> 注意：函数体内的第一行字符串 = `__doc__`。

## 1.2 `__init__` vs `__new__`

| | `__new__` | `__init__` |
|---|---|---|
| 何时调用 | **创建实例时**（最早） | 实例已创建、初始化时 |
| 第一个参数 | `cls` | `self` |
| 责任 | 真正"造"出实例 | 给实例赋值 |
| 何时重写 | 不可变子类、单例、缓存实例 | 99% 的情况 |

```python
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = Singleton()
s2 = Singleton()
s1 is s2   # True
```

**99% 的情况只需要 `__init__`**。能写 `__init__` 就不写 `__new__`。

## 1.3 继承

```python
class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return "..."

class Dog(Animal):
    def speak(self) -> str:
        return "Woof"

d = Dog("Rex")
d.speak()       # "Woof"
d.name          # "Rex"   来自 Animal
```

子类自动继承父类的所有属性、方法。

## 1.4 `super()`：调父类方法

```python
class Dog(Animal):
    def __init__(self, name: str, breed: str) -> None:
        super().__init__(name)     # 调用 Animal.__init__
        self.breed = breed
```

`super()` 在 Python 3 里 = `super().__init__(...)`（自动填 cls/self）。

**不要硬编码父类名**：

```python
# 错
class Dog(Animal):
    def __init__(self, name, breed):
        Animal.__init__(self, name)    # 改继承结构时崩
        self.breed = breed

# 对
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)         # 永远正确
        self.breed = breed
```

## 1.5 MRO（方法解析顺序）

Python 用 **C3 线性化**算法计算 MRO。`Class.mro()` 返回方法查找顺序：

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

D.mro()
# [D, B, C, A, object]
```

查找 `d.x` 时按这个顺序找。

**菱形问题**：

```
    A
   / \
  B   C
   \ /
    D
```

`D` 同时继承 `B` 和 `C`，`B` 和 `C` 都继承 `A`。C3 保证：

- 子类优先于父类
- 父类按声明顺序
- 单调性（子类顺序不影响祖先顺序）

## 1.6 多继承中的 `super()`

```python
class A:
    def m(self):
        print("A.m")
        return "A"

class B(A):
    def m(self):
        print("B.m")
        return super().m() + "+B"

class C(A):
    def m(self):
        print("C.m")
        return super().m() + "+C"

class D(B, C):
    def m(self):
        print("D.m")
        return super().m() + "+D"

D().m()
# D.m
# B.m
# C.m
# A.m
# 返回 "A+C+B+D"
```

每个 `super()` 都按 MRO 找下一个。**永远不调用"父类"，调用"MRO 中的下一个"**。

## 1.7 `isinstance` / `issubclass`

```python
isinstance(d, Dog)         # True
isinstance(d, Animal)      # True   (Dog 继承 Animal)
isinstance(d, object)      # True   一切都是 object

issubclass(Dog, Animal)    # True
```

`isinstance` 走 `__instancecheck__`（默认走 MRO），可以重写——阶段 3 高级话题。

## 1.8 类属性 vs 实例属性

```python
class Counter:
    default = 0                  # 类属性

    def __init__(self):
        self.count = 0           # 实例属性

c = Counter()
c.default    # 0   （实例没找到，去类找）
Counter.default = 10
c.default    # 10  （类属性变了，所有实例可见）

c.count = 5
c.count      # 5
```

**坑**：可变类属性被所有实例共享。

```python
class Bag:
    items = []                   # 错

    def add(self, x):
        self.items.append(x)     # 所有实例共享同一个 list

# 对
class Bag:
    def __init__(self):
        self.items = []          # 每个实例自己的
```

## 1.9 方法类型

```python
class A:
    def instance_m(self): ...    # 实例方法：第一个参数是 self
    @classmethod
    def class_m(cls): ...        # 类方法：第一个参数是 cls
    @staticmethod
    def static_m(): ...          # 静态方法：无 self/cls
    @property
    def prop(self): ...          # 属性：像属性一样访问
```

> 阶段 3-2 详解方法在字节码层的真相。

## 1.10 `__init_subclass__`（3.6+）

子类被创建时自动调用：

```python
class Plugin:
    plugins: list[type] = []

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        Plugin.plugins.append(cls)

class A(Plugin): pass
class B(Plugin): pass

Plugin.plugins   # [A, B]
```

`dataclasses.dataclass` / `attrs` / Django ORM 都用这个。

## 1.11 `__class__` 与 unbound method

```python
class A:
    def m(self):
        return self.__class__.__name__   # 推荐写法
```

`A.m` 在 Python 3 里就是普通函数（不再是"unbound method"）。

## 1.12 `type` 与 metaclass

`type(name, bases, namespace)` 动态创建类：

```python
MyClass = type("MyClass", (object,), {"x": 1, "y": 2})
```

metaclass = "类的类"。阶段 3 不深入（真实项目 99% 不会写 metaclass），可参考 [06-multiple-inheritance.md](./06-multiple-inheritance.md) 末尾的简短介绍。
