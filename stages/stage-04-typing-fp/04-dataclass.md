# 04 - `@dataclass`

`@dataclass` 是写小数据类的官方推荐方式。它生成 `__init__` / `__repr__` / `__eq__`，还支持 frozen、slots、default factory。

## 4.1 基础

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p = Point(1.5, 2.5)              # 自动 __init__
p                                # Point(x=1.5, y=2.5)   自动 __repr__
Point(1, 2) == Point(1, 2)       # True                  自动 __eq__
```

`@dataclass` 默认**可变**。

## 4.2 默认值

```python
@dataclass
class User:
    name: str
    age: int = 0
    tags: list[str] = field(default_factory=list)    # 关键！
```

**坑**：直接 `tags: list[str] = []` 会让所有实例共享同一个 list（阶段 1 讲过）。用 `default_factory`。

## 4.3 `frozen=True`：不可变

```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1, 2)
p.x = 3                            # FrozenInstanceError
hash(p)                            # 可哈希
```

`frozen=True` 触发 `__hash__` 生成，可以放进 `set` / `dict` 当 key。

## 4.4 `slots=True`：消除 `__dict__`（3.10+）

```python
@dataclass(slots=True)
class Point:
    x: float
    y: float

p = Point(1, 2)
p.__dict__                         # AttributeError
p.z = 3                            # AttributeError
```

省内存、防动态加字段。**阶段 3 已学**。

## 4.5 `__post_init__`：校验与派生字段

```python
@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("amount must be >= 0")
        if len(self.currency) != 3:
            raise ValueError("currency must be 3-letter code")
```

`frozen=True` 时**仍可**在 `__post_init__` 内修改（用 `object.__setattr__`）：

```python
@dataclass(frozen=True)
class Money:
    amount: float
    currency: str
    upper_currency: str = ""

    def __post_init__(self) -> None:
        if not self.upper_currency:
            object.__setattr__(self, "upper_currency", self.currency.upper())
```

## 4.6 `field()`：字段元信息

```python
from dataclasses import dataclass, field

@dataclass
class Article:
    title: str
    body: str = field(repr=False)        # 不在 __repr__ 里
    tags: list[str] = field(default_factory=list)
    author: str = field(compare=False)   # 不参与 __eq__
    _id: int = field(init=False)         # 不在 __init__ 里

    def __post_init__(self) -> None:
        self._id = id(self)              # 派生
```

`field()` 选项：

| 选项 | 作用 |
|---|---|
| `default` | 默认值 |
| `default_factory` | 可变默认值的工厂 |
| `init=True/False` | 是否进 `__init__` |
| `repr=True/False` | 是否进 `__repr__` |
| `compare=True/False` | 是否进 `__eq__` |
| `hash=None/True/False` | 哈希相关 |
| `metadata` | 任意 dict（第三方库读） |

## 4.7 继承

```python
@dataclass
class Animal:
    name: str

@dataclass
class Dog(Animal):
    breed: str
```

`Dog("Rex", "Husky")` 调用 `Animal.__init__` + 设置 `breed`。

**坑**：父类有默认值，子类字段会触发"non-default after default"错误：

```python
@dataclass
class Animal:
    name: str = "unknown"     # 默认值

@dataclass
class Dog(Animal):
    breed: str                # 报错：non-default after default
```

解：父类字段都加默认值，或子类也加。

## 4.8 `KW_ONLY`（3.10+）：强制关键字参数

```python
from dataclasses import dataclass, KW_ONLY

@dataclass
class User:
    name: str
    _: KW_ONLY
    age: int                  # 必须用 keyword
    email: str = "n/a"

User("alice", age=30)         # OK
User("alice", 30)             # TypeError
```

防止位置参数顺序误用。

## 4.9 `asdict` / `astuple` / `replace`

```python
from dataclasses import asdict, astuple, replace

p = Point(1, 2)
asdict(p)                     # {'x': 1, 'y': 2}
astuple(p)                    # (1, 2)
p2 = replace(p, x=10)         # Point(10, 2)   不改原对象
```

`replace` = "不可变对象的 copy with change"。

## 4.10 排序支持

`@dataclass` 默认**不可排序**。要 `<` / `>`，加 `order=True`：

```python
@dataclass(order=True)
class Version:
    major: int
    minor: int

Version(1, 5) < Version(2, 0)            # True
```

`order=True` 用字段顺序比较（类似 `tuple`）。

## 4.11 `unsafe_hash`

`@dataclass(eq=True)` 默认 `__hash__ = None`（因为可变）。要哈希：

```python
@dataclass(frozen=True)       # 自动 __hash__
class P: ...

@dataclass(unsafe_hash=True)   # 强制 __hash__，但小心可变对象
class Q: ...
```

## 4.12 `InitVar`：仅在 `__init__` 用

```python
@dataclass
class User:
    name: str
    password_hash: str = field(init=False)
    password: InitVar[str] = ""              # 仅在 __init__

    def __post_init__(self, password: str) -> None:
        if password:
            self.password_hash = hash(password)
```

`InitVar` 是构造时临时用的，不进 `__init__` 参数、不存到实例。

## 4.13 完整例子

```python
from dataclasses import dataclass, field, KW_ONLY
from typing import ClassVar

@dataclass(frozen=True, slots=True)
class Coordinate:
    x: float
    y: float
    z: float = 0.0

    _origin: ClassVar["Coordinate"] = None   # 类级缓存

    def __post_init__(self) -> None:
        if self._origin is None:
            Coordinate._origin = Coordinate(0, 0, 0)

c = Coordinate(1, 2, 3)
c2 = c.replace(z=10)
Coordinate._origin                         # Coordinate(0, 0, 0)
```

## 4.14 与其他库的对比

| 库 | 特点 |
|---|---|
| `@dataclass` | 标准库、零依赖、最快 |
| `attrs` | 比 dataclass 早、更多特性（validators、converters） |
| `pydantic` | 运行时验证、JSON 序列化、Web 框架首选 |
| `msgspec` | 极快、struct 风格 |

阶段 6 详讲 pydantic / msgspec。
