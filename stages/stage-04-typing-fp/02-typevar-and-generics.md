# 02 - TypeVar 与泛型

## 2.1 泛型的直觉

```python
def first(xs: list[int]) -> int:
    return xs[0]
```

`first(["a", "b"])` mypy 报错。"只接受 int 列表"是限制。

**泛型** = "类型参数化"——让函数能接受任意类型，同时保留类型信息：

```python
from typing import TypeVar

T = TypeVar("T")

def first(xs: list[T]) -> T:
    return xs[0]

first([1, 2, 3])            # int
first(["a", "b"])           # str
```

`mypy` 会按调用推断出 `T` 的具体类型。

## 2.2 `TypeVar`：声明类型变量

```python
T = TypeVar("T")                        # 不约束
T = TypeVar("T", bound=int)             # 必须是 int 或子类
T = TypeVar("T", int, str, float)       # 必须是这几个之一（具体值约束）
T = TypeVar("T", covariant=True)        # 协变（输出位置）
T = TypeVar("T", contravariant=True)    # 逆变（输入位置）
```

**位置不变（默认）**：

```python
T = TypeVar("T")
def first(xs: list[T]) -> T: ...        # 不可变
```

**协变**（仅作输出，比如 `Sequence`）：

```python
T_co = TypeVar("T_co", covariant=True)
class Box(Generic[T_co]):
    def get(self) -> T_co: ...          # 只输出 T_co
```

**逆变**（仅作输入，比如 `Comparable`）：

```python
T_contra = TypeVar("T_contra", contravariant=True)
class Sink(Generic[T_contra]):
    def consume(self, x: T_contra) -> None: ...
```

## 2.3 `Generic[T]`：泛型类

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

s = Stack[int]()
s.push(1)
x: int = s.pop()

s2 = Stack[str]()
s2.push("hello")
```

> 阶段 4 末的 PEP 695（Python 3.12+）有更简洁的语法：`class Stack[T]:`。

## 2.4 多类型参数

```python
K = TypeVar("K")
V = TypeVar("V")

class Pair(Generic[K, V]):
    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value

    def swap(self) -> "Pair[V, K]":
        return Pair(self.value, self.key)

p: Pair[str, int] = Pair("age", 30)
p2 = p.swap()              # Pair[int, str]
```

## 2.5 协议 + 泛型：常见模式

```python
from typing import Protocol, TypeVar

T = TypeVar("T")
U = TypeVar("U")

class Transformer(Protocol[T, U]):
    def transform(self, x: T) -> U: ...

# 实现不需要 Generic 注解——Protocol 是结构化的
class StrToInt:
    def transform(self, x: str) -> int:
        return int(x)

# isinstance 检查：Protocol 不需要 Generic 标记
def run(t: Transformer[str, int], x: str) -> int:
    return t.transform(x)
```

## 2.6 `ParamSpec`：保留函数签名

装饰器要保留 `*args` / `**kwargs` 的类型时用：

```python
from typing import ParamSpec, TypeVar, Callable

P = ParamSpec("P")
R = TypeVar("R")

def timer(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.perf_counter() - start:.3f}s")
        return result
    return wrapper

@timer
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)        # mypy 仍知道 add 接受 (int, int) -> int
```

阶段 2 装饰器的类型化版本。

## 2.7 泛型 + `TypeVarTuple`（3.11+）：异构 tuple

```python
from typing import TypeVarTuple, Generic

Ts = TypeVarTuple("Ts")

class Struct(Generic[*Ts]):
    def __init__(self, *args: *Ts) -> None: ...
    def values(self) -> tuple[*Ts]: ...

s: Struct[int, str, float] = Struct(1, "x", 1.0)
```

阶段 4 项目不会用到，提一下。

## 2.8 PEP 695：Python 3.12+ 新语法

3.12 起，泛型语法大幅简化：

```python
# 旧
T = TypeVar("T")
class Stack(Generic[T]): ...

# 新（PEP 695）
class Stack[T]: ...                    # 自动是 Generic[T]
type ListOrSet[T] = list[T] | set[T]  # 替代 TypeAlias
def first[T](xs: list[T]) -> T: ...   # 函数泛型
```

`TypeVar` 不再需要显式声明，**类型形参自动推断**。

## 2.9 实战：`Result[T, E]`

```python
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")

class Ok(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
    def __repr__(self) -> str:
        return f"Ok({self.value!r})"

class Err(Generic[E]):
    def __init__(self, error: E) -> None:
        self.error = error
    def __repr__(self) -> str:
        return f"Err({self.error!r})"

Result = Ok[T] | Err[E]                # 3.10+

# 实际代码（Rust / Go / Haskell 常见）
def safe_div(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)
```

## 2.10 选型指南

| 需求 | 用 |
|---|---|
| 容器接受任意类型 | `Generic[T]` |
| 函数参数保持类型 | `TypeVar` |
| 装饰器保留签名 | `ParamSpec` |
| 协变（只输出） | `TypeVar("T", covariant=True)` |
| 逆变（只输入） | `TypeVar("T", contravariant=True)` |
| Python 3.12+ | PEP 695 内联语法 |
