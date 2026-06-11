# 01 - typing 基础

## 1.1 为什么用类型提示

- **自动文档**：签名自带"字段说明"
- **静态检查**：`mypy` / `pyright` 在运行前抓 bug
- **IDE 辅助**：补全、重构、跳转
- **重构安全**：改一处类型不匹配会立刻暴露

```python
def add(a: int, b: int) -> int:
    return a + b
```

不需要 import、运行时零开销。

## 1.2 内置容器（3.9+）

```python
# 现代写法（3.9+）
def f(xs: list[int]) -> dict[str, int]:
    ...

# 老写法（仍支持，但不推荐）
from typing import List, Dict
def f(xs: List[int]) -> Dict[str, int]: ...
```

**所有内置容器**都可以直接参数化：

```python
list[int]
set[str]
tuple[int, str, float]      # 固定长度
tuple[int, ...]             # 任意长度（同构）
dict[str, int]
type[int]                   # 3.12+，原来要用 Type[int]
```

## 1.3 `Optional` / `Union` / `|`（3.10+）

```python
from typing import Optional, Union

# Optional[X] = Union[X, None]
def find(id: str) -> Optional[User]: ...

# Python 3.10+ 可以直接 |
def find(id: str) -> User | None: ...
```

```python
# 多个类型
def parse(s: str) -> int | float | None: ...

# 3.10+ 用 Union[X, Y] 仍可，但 | 更短
```

## 1.4 `Literal`：限定值

```python
from typing import Literal

Level = Literal["INFO", "WARN", "ERROR"]

def log(level: Level, msg: str) -> None: ...

log("INFO", "ok")           # OK
log("DEBUG", "x")           # mypy 报错
```

阶段 5（async）、网络层（method）、CLI（command）大量使用。

## 1.5 `TypedDict`：dict 的形状

```python
from typing import TypedDict

class UserDict(TypedDict):
    name: str
    age: int

u: UserDict = {"name": "alice", "age": 30}      # OK
u: UserDict = {"name": "alice"}                  # mypy 报错：缺 age
```

用于"JSON-like 数据"，而不是真正的类（用 `dataclass` 更适合"领域对象"）。

**带可选字段**：

```python
class UserDict(TypedDict, total=False):
    name: str       # total=False 全部可选
    age: int

# total=True（默认）所有字段必填
class StrictUser(TypedDict):
    name: str
    age: int
```

## 1.6 `NewType`：逻辑上的"新类型"

```python
from typing import NewType

UserId = NewType("UserId", int)
Email = NewType("Email", str)

def get_user(uid: UserId) -> User: ...
def get_by_email(e: Email) -> User: ...

uid = UserId(42)
get_user(uid)             # OK
get_user(42)              # mypy 报错：int 不是 UserId
```

**运行时零开销**（就是 `int` 本身），只用于静态检查。

## 1.7 `TypeAlias`：给复杂类型起名

```python
from typing import TypeAlias

JsonValue: TypeAlias = (
    None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
)

Coordinates: TypeAlias = tuple[float, float]
```

3.10+ 可以用 `type` 关键字（PEP 695，阶段 4 末会讲）。

## 1.8 `Final`：常量

```python
from typing import Final

MAX_SIZE: Final = 1000
MAX_SIZE = 2000            # mypy 报错
```

## 1.9 `Annotated`：附加元数据

```python
from typing import Annotated

# 第三方库（FastAPI / Pydantic）读这些元数据
def add(
    name: Annotated[str, "用户姓名"],
    age: Annotated[int, "年龄", ">= 0"],
) -> None: ...
```

`Annotated[T, metadata1, metadata2, ...]` —— `T` 是类型，剩下的是附加信息（运行时可通过 `get_type_hints` 读取）。

## 1.10 `Any`：逃生口

```python
from typing import Any

def legacy_func(data: Any) -> Any: ...
```

`Any` 关掉类型检查。**少用**——一旦标 `Any`，后面全无检查。

## 1.11 `cast`：显式断言

```python
from typing import cast

x: object = "hello"
s = cast(str, x)           # mypy 信你，不再报
s.upper()                  # OK
```

`cast` 不做运行时检查，纯粹告诉 mypy "我比你懂"。

## 1.12 阶段 4 项目中的常见类型

```python
# 输入：dict（JSON / CSV 行）
RawRecord = dict[str, object]

# 阶段 1：解析后
@dataclass(frozen=True)
class ParsedRecord:
    user_id: int
    timestamp: str
    action: str

# 阶段 2：校验后
@dataclass(frozen=True)
class ValidatedRecord:
    user_id: UserId            # NewType
    timestamp: str
    action: Action             # Literal

# 阶段 3：富化后
@dataclass(frozen=True)
class EnrichedRecord:
    user_id: UserId
    timestamp: datetime
    action: Action
    weekday: str               # 派生

# 阶段 4：汇总
@dataclass(frozen=True)
class Summary:
    total: int
    by_action: dict[Action, int]
```

## 1.13 速查

| 场景 | 用 |
|---|---|
| 容器 | `list[T]` / `dict[K, V]` / `set[T]` / `tuple[T, ...]` |
| 可能为 None | `T \| None`（3.10+） |
| 多类型 | `T \| U` |
| 限定值 | `Literal["a", "b"]` |
| 字典形状 | `TypedDict` |
| 逻辑子类型 | `NewType` |
| 复杂类型别名 | `TypeAlias` |
| 常量 | `Final` |
| 元数据 | `Annotated` |
| 逃生 | `Any` / `cast` |
