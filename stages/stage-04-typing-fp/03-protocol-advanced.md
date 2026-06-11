# 03 - Protocol 进阶

## 3.1 阶段 3 回顾

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class SupportsClose(Protocol):
    def close(self) -> None: ...
```

阶段 4 讲更"工程化"的用法。

## 3.2 `Self`（3.11+）：返回自身类型

**问题**：`__add__` 应该返回"自身的精确类型"（包括子类）：

```python
class MyList:
    def __add__(self, other) -> "MyList": ...       # 写死父类
```

子类 `BetterList(MyList)` 相加时返回的还是 `MyList`，类型丢了。

**解法（3.11+）**：

```python
from typing import Self

class MyList:
    def __add__(self, other) -> Self:
        ...
```

`Self` 自动替换为"调用方的实际类型"。

## 3.3 组合 Protocol

```python
class Readable(Protocol):
    def read(self) -> str: ...

class Writable(Protocol):
    def write(self, data: str) -> None: ...

class ReadWritable(Readable, Writable, Protocol):
    pass

def process(stream: ReadWritable) -> None:
    data = stream.read()
    stream.write(data.upper())
```

## 3.4 Protocol + `TypeVar`：泛型协议

```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class Converter(Protocol[T]):
    def convert(self, x: str) -> T: ...

# 实现不需要 Generic 标注
class IntConverter:
    def convert(self, x: str) -> int:
        return int(x)

class StrConverter:
    def convert(self, x: str) -> str:
        return x

def run(c: Converter[int], x: str) -> int:
    return c.convert(x)
```

## 3.5 协议 + 抽象方法（不推荐混用）

```python
class Foo(ABC, Protocol):           # 合法但少见
    @abstractmethod
    def m(self) -> None: ...
```

`Protocol` 表达"形状"，`ABC` 表达"必须继承"。**99% 选其中一个**。

## 3.6 `@runtime_checkable` 的局限

```python
@runtime_checkable
class HasName(Protocol):
    name: str                       # 属性（不是方法）
    def close(self) -> None: ...

class C:
    name = "x"
    def close(self): pass

isinstance(C(), HasName)           # True   检查 name 存在 + close 存在
hasattr(C(), "name") and hasattr(C(), "close")
```

**只检查"名字在不在"**，不检查签名（参数、返回类型）。

## 3.7 实战：框架的"接口"用 Protocol

```python
class Repository(Protocol):
    def get(self, id: str) -> dict: ...
    def save(self, data: dict) -> None: ...
    def delete(self, id: str) -> None: ...

class UserService:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo
```

`UserService` 接受任何实现 `Repository` 三方法的类：`InMemoryRepo` / `PostgresRepo` / `MockRepo` 都可以。

## 3.8 协议 + 协变 / 逆变

```python
class Producer(Protocol[T_co]):    # 协变：返回 T
    def produce(self) -> T_co: ...

class Consumer(Protocol[T_contra]): # 逆变：接收 T
    def consume(self, x: T_contra) -> None: ...
```

阶段 2-3 不强求；用 `mypy --strict` 自动检查。

## 3.9 真实工程例子

### Django 的 `QuerySet` 协议

```python
class QuerySetLike(Protocol):
    def filter(self, **kwargs) -> "QuerySetLike": ...
    def all(self) -> "QuerySetLike": ...
    def __iter__(self): ...
```

任何支持这些方法的"查询对象"都能用。

### SQLAlchemy 的 `Session` 协议

```python
class SessionLike(Protocol):
    def add(self, obj: object) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
```

测试时传 `MockSession` 即可。

## 3.10 选型决策树

```
需要"形状"接口（解耦业务）  → Protocol
需要"必须继承"接口（框架）  → ABC
需要"运行时检查"           → runtime_checkable Protocol
需要"必须实现才能实例化"   → ABC + @abstractmethod
都不需要                    → 直接调（鸭子类型）
```

## 3.11 阶段 4 项目怎么用

数据管线的转换器：

```python
class Transformer(Protocol[T, U]):
    def transform(self, x: T) -> U: ...

class Validator(Protocol[T]):
    def validate(self, x: T) -> T | None: ...
```

让用户写自己的实现，不用继承基类。
