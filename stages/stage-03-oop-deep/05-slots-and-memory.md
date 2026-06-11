# 05 - `__slots__` 与内存

## 5.1 默认情况：实例有 `__dict__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
p.__dict__        # {'x': 1, 'y': 2}
p.z = 3           # 任意加属性
p.__dict__        # {'x': 1, 'y': 2, 'z': 3}
```

每个实例有自己的 `dict` 存属性。灵活但费内存。

## 5.2 `__slots__`：固定属性集

```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
p.__dict__        # AttributeError
p.z = 3           # AttributeError: 'Point' object has no attribute 'z'
```

加了 `__slots__` 后：

- 实例**没有 `__dict__`**
- 只能有 `__slots__` 列出的属性
- 属性查找走 slot descriptor（数组式存储）

## 5.3 内存差距有多大？

```python
import sys

class WithDict:
    def __init__(self):
        self.x = 1
        self.y = 2

class WithSlots:
    __slots__ = ("x", "y")
    def __init__(self):
        self.x = 1
        self.y = 2

sys.getsizeof(WithDict())      # ~56 字节（实例 + 字典指针）
sys.getsizeof(WithSlots())     # ~48 字节

# 字典本身又占内存
import tracemalloc
# 一百万个实例：slots 比 dict 少 30%-50%
```

实际差距比 `getsizeof` 看到的更大（dict 内部还有哈希表开销）。

## 5.4 访问速度

```python
import timeit

t1 = timeit.timeit("p.x", globals={"p": WithDict()})   # ~0.07us
t2 = timeit.timeit("p.x", globals={"p": WithSlots()})  # ~0.05us
```

slots 略快（避免 dict 查找），但对纯 Python 代码通常不是瓶颈。

## 5.5 什么时候**不**用 `__slots__`

- 需要动态加属性（dict 风格的灵活性）
- 类会被 monkey-patch
- 类用了 `@dataclass`（**会冲突**——见下）
- 类在继承链上要让子类加属性

## 5.6 与继承

```python
class Base:
    __slots__ = ("a",)

class Child(Base):
    __slots__ = ("b",)

c = Child()
c.a = 1      # OK
c.b = 2      # OK
c.c = 3      # AttributeError
```

**关键规则**：

- 父类有 `__slots__`、子类**也声明** `__slots__`：子类实例**没有** `__dict__`
- 父类有 `__slots__`、子类**不声明** `__slots__`：子类实例**有** `__dict__`

**所有想消除 `__dict__` 的类都要声明 `__slots__`**。

## 5.7 `__dict__` vs `__slots__` vs `__weakref__`

- 默认：`__dict__` + `__weakref__`（`weakref.ref()` 可用）
- 加 `__slots__`：去掉 `__dict__` + `__weakref__`（除非显式列）
- 显式 `__slots__ = ("a", "__dict__")`：保留 dict

```python
class WithWeakRef:
    __slots__ = ("x", "__weakref__")   # 允许 weakref

class NoWeakRef:
    __slots__ = ("x",)                 # 不允许 weakref
```

## 5.8 与 `@dataclass` 的冲突

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```

`@dataclass` 默认给每个实例 `__dict__`。如果想用 slots + dataclass：

```python
@dataclass(slots=True)     # 3.10+
class Point:
    x: int
    y: int
```

阶段 4 详讲 `dataclass`。

## 5.9 命名元组：最紧凑的"小数据类"

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

p = Point(1, 2)
p.x, p.y         # (1, 2)
p[0], p[1]       # (1, 2)
p._asdict()      # {'x': 1, 'y': 2}
```

`NamedTuple` 本质是 `tuple` 子类：不可变、有 slots、自动有 `__eq__` / `__repr__` / `__iter__`。

**当数据是不可变 + 字段数 ≤ 5 时，优先用 `NamedTuple`**。

## 5.10 选型指南

| 场景 | 推荐 |
|---|---|
| 几百万个小数据对象 | `__slots__` 或 `NamedTuple` |
| 普通业务类 | 不加 `__slots__`（灵活优先） |
| 不可变 + 少量字段 | `NamedTuple` |
| 不可变 + dataclass 行为 | `@dataclass(frozen=True, slots=True)` |
| 配置对象 / DTO | `@dataclass(slots=True)` |
| 框架内部"小对象" | `__slots__` |

## 5.11 总结

- `__slots__` 牺牲灵活性换内存 / 略快
- 子类想消除 `__dict__` 必须**自己**也声明
- 实际项目：瓶颈通常在数据结构选型，slots 只是锦上添花
- 真实的高性能场景：考虑 `__slots__` + `attrs` / `pydantic` / 干脆用 Cython
