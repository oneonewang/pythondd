# 05 - 魔术方法（dunder methods）

"魔术方法" = 双下划线开头结尾的方法，让你自定义类型表现得像内置类型。

## 5.1 核心原则

- 只在真的需要时实现 dunder。多了反而乱。
- `__repr__` 几乎必写（调试 + REPL）
- `__eq__` 写了一定要写 `__hash__`（阶段 3 详讲）

## 5.2 速查

| 协议 | 方法 | 触发 |
|---|---|---|
| 字符串表示 | `__repr__`, `__str__`, `__format__` | `repr(obj)`, `str(obj)`, `f"{obj:>5}"` |
| 布尔 | `__bool__` | `if obj`, `not obj` |
| 比较 | `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`, `__hash__` | `==`, `<`, `set`, `dict key` |
| 长度 | `__len__` | `len(obj)` |
| 迭代 | `__iter__`, `__next__` | `for x in obj`, `iter(obj)`, `next(obj)` |
| 容器 | `__getitem__`, `__setitem__`, `__delitem__`, `__contains__` | `obj[k]`, `k in obj` |
| 调用 | `__call__` | `obj()` |
| 上下文 | `__enter__`, `__exit__` | `with obj:` |
| 构造 | `__new__`, `__init__`, `__del__` | `MyClass(...)` |
| 属性 | `__getattr__`, `__setattr__`, `__getattribute__`, `__dir__` | `obj.attr` |
| 描述符 | `__get__`, `__set__`, `__delete__` | 类属性访问（阶段 3 详讲） |
| 算术 | `__add__`, `__mul__`, `__radd__`, `__iadd__` | `+`, `*`, 反射, 原地 |
| 数值转换 | `__int__`, `__float__`, `__index__` | `int(obj)`, `list[i]` |
| 拷贝 | `__copy__`, `__deepcopy__` | `copy.copy/deepcopy` |
| 哈希 | `__hash__` | `hash(obj)` |

## 5.3 `__repr__` / `__str__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
```

- `__repr__` 给开发者看：**无歧义、可重新构造**（`Point(x=1, y=2)`）
- `__str__` 给用户看：可读
- 没写 `__str__` 时，`str(obj)` 退到 `__repr__`

## 5.4 `__eq__` 与 `__hash__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))
```

> 经验：自定义 `__eq__` 后，对象**默认不可哈希**（`hash` 抛 `TypeError`）。要么显式 `__hash__ = None` 禁止哈希，要么写一个能跟 `__eq__` 一致的 `__hash__`。

**重写**：
- `dataclass(eq=True)` 会自动写 `__eq__` 但把 `__hash__` 置为 None（可哈希的对象用 `@dataclass(eq=False, frozen=True)`）
- 阶段 4 详讲

## 5.5 `__len__` 与 `__bool__`

```python
class Bag:
    def __init__(self, items):
        self._items = list(items)

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return bool(self._items)
```

> 经验：`__bool__` 优先于 `__len__`；只写 `__len__` 时，0 是 False、非 0 是 True。

## 5.6 `__getitem__` / `__setitem__` / `__contains__`

```python
class Matrix:
    def __init__(self, rows, cols, default=0):
        self._data = [[default] * cols for _ in range(rows)]
        self._shape = rows, cols

    def __getitem__(self, key):
        r, c = key
        return self._data[r][c]

    def __setitem__(self, key, value):
        r, c = key
        self._data[r][c] = value

    def __contains__(self, value):
        return any(value in row for row in self._data)
```

写 `__getitem__` 之后，**Python 自动提供迭代**（按 0, 1, 2, ... 调 `__getitem__` 直到 `IndexError`）。所以 `for x in matrix` 也能用，但慢。

## 5.7 `__iter__` 比 `__getitem__` 优先

```python
class MyList:
    def __init__(self, items): self._items = items
    def __iter__(self): return iter(self._items)
    # for x in obj 调用 __iter__，不再用 __getitem__
```

> 经验：要让对象能 `for`，**优先** `__iter__`，**次之** `__getitem__`。

## 5.8 `__call__`

让对象像函数一样被调用。

```python
class Greeter:
    def __init__(self, greeting): self.greeting = greeting
    def __call__(self, name): return f"{self.greeting}, {name}"

hello = Greeter("Hello")
hello("alice")     # "Hello, alice"
```

用途：可调用对象携带状态（比闭包更易测试、可序列化）。框架里大量使用（PyTorch 的 `nn.Module`、`functools.partial` 风格的 `partial`、Django 的中间件类）。

## 5.9 `__enter__` / `__exit__`

见 [04-context-managers.md](./04-context-managers.md)。

## 5.10 富比较（`__lt__` 等）

`@total_ordering` 一行搞定：

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, major, minor):
        self.major, self.minor = major, minor

    def __eq__(self, other): return (self.major, self.minor) == (other.major, other.minor)
    def __lt__(self, other): return (self.major, self.minor) < (other.major, other.minor)
```

有了 `__eq__` 和 `__lt__`，`<=` / `>` / `>=` 自动可用。

## 5.11 `__add__` 与反射 `__radd__`

```python
class Vec2:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, other): return Vec2(self.x + other.x, self.y + other.y)
    def __radd__(self, other): return self.__add__(other)   # sum() 起始值是 0

v = Vec2(1, 2)
sum([v, v, v])  # OK
```

## 5.12 `__init__` vs `__new__`

- `__new__` 创建实例（很少用，**不可变子类、metaclass、缓存实例**才需要）
- `__init__` 初始化实例（绝大多数情况只用这个）

## 5.13 调试输出最佳实践

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
```

`@dataclass` 自动生成 `__init__` / `__repr__` / `__eq__`，**是阶段 2 之后写小数据类的首选**。阶段 4 详讲。
