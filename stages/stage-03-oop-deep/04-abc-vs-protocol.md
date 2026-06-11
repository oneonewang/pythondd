# 04 - ABC vs Protocol

两种"接口"方式：传统 ABC（`abc.ABCMeta`） vs 现代 Protocol（结构化子类型）。

## 4.1 抽象基类（ABC）

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
    @abstractmethod
    def perimeter(self) -> float: ...

    def describe(self) -> str:                  # 可有具体方法
        return f"area={self.area():.2f}"

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2
    def perimeter(self): return 2 * 3.14 * self.r

Circle(1)              # OK
Shape()                # TypeError: Can't instantiate abstract class
```

**特点**：

- 必须显式继承才能成为 ABC 子类
- 没实现抽象方法的子类**不能实例化**
- `isinstance(obj, Shape)` 对子类返回 True
- 可以有具体方法

## 4.2 内部机制

ABC 用 `ABCMeta` 作为 metaclass。`@abstractmethod` 把方法标记为抽象，且**实例化时检查**所有抽象方法都已实现。

```python
class Shape(metaclass=ABCMeta):                # 等价
    @abstractmethod
    def area(self): ...
```

## 4.3 注册虚拟子类

不想改源码但想"认"为是某 ABC 的子类：

```python
Shape.register(dict)              # dict 现在算 Shape
isinstance({}, Shape)             # True
```

只影响 `isinstance` / `issubclass`，不影响继承树。

## 4.4 `Protocol`（PEP 544）

```python
from typing import Protocol

class SupportsClose(Protocol):
    def close(self) -> None: ...

def close_all(things: list[SupportsClose]) -> None:
    for t in things:
        t.close()

class File:
    def close(self) -> None: print("file closed")
class Connection:
    def close(self) -> None: print("conn closed")

close_all([File(), Connection()])    # mypy 通过；运行也通过
```

**`File` 没继承 `SupportsClose`，但形状一致 → 结构化子类型**。

## 4.5 `runtime_checkable`

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class SupportsClose(Protocol):
    def close(self) -> None: ...

isinstance(File(), SupportsClose)         # True
isinstance("not closeable", SupportsClose) # False
```

不装饰的 Protocol 只能静态检查（mypy），不能 `isinstance` 验证。

> 注意：`runtime_checkable` 只检查"方法名存不存在"，不检查签名。

## 4.6 何时用哪个

| 场景 | 选择 | 理由 |
|---|---|---|
| 你写的库 / 框架内部 | **ABC** | 强制实现、防止误用、清晰继承关系 |
| 第三方代码 / 鸭子类型场景 | **Protocol** | 不强迫他们改代码 |
| 只想声明"我接受任何 close() 东西" | **Protocol** | 表达意图、不绑继承 |
| 既有继承又有新代码 | 都有用 | ABC 给老代码，Protocol 给新代码 |
| 框架设计：给"插件"作者看的接口 | **ABC** | 让他们"必须实现" |
| 内部辅助函数 / 数据处理 | **Protocol** | 简洁、不绑死 |

## 4.7 实际例子

### ABC 用例：Django Model

```python
class Model(metaclass=ABCMeta):
    @abstractmethod
    def save(self): ...
    @abstractmethod
    def delete(self): ...

class User(Model):
    def save(self): ...    # 必须实现
    def delete(self): ...
```

继承模型清晰，框架用 `isinstance(obj, Model)` 做判断。

### Protocol 用例：业务逻辑解耦

```python
class Repository(Protocol):
    def get(self, id: str) -> dict: ...
    def save(self, data: dict) -> None: ...

class UserService:
    def __init__(self, repo: Repository):
        self.repo = repo            # 任何实现这俩方法的都行
```

`repo` 可以是 `PostgresRepo` / `MongoRepo` / `InMemoryRepo` / 任何 mock，不绑继承。

## 4.8 `Protocol` + 泛型

```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class Comparable(Protocol):
    def __lt__(self, other: "Comparable") -> bool: ...

def sort(items: list[T]) -> list[T]:
    return sorted(items)    # 要求 T 实现 Comparable
```

## 4.9 多个 Protocol 组合

```python
class Readable(Protocol):
    def read(self) -> str: ...

class Writable(Protocol):
    def write(self, data: str) -> None: ...

class ReadWritable(Readable, Writable, Protocol): ...

def process(stream: ReadWritable) -> None:
    data = stream.read()
    stream.write(data.upper())
```

## 4.10 总结

- **ABC**：显式继承 + 强制实现 + 适合框架
- **Protocol**：鸭子类型 + 结构化子类型 + 适合业务解耦
- 大多数新代码，**Protocol 优先**；需要"必须实现"用 ABC
- `runtime_checkable` 让 Protocol 也能 `isinstance`，但只是"鸭子识别"

## 4.11 阶段 3 项目怎么用

规则引擎用 `Protocol` 定义 `Rule` 接口：让用户写"形状对"的规则类即可，不用继承任何基类。
