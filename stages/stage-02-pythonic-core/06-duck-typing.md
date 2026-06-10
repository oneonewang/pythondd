# 06 - 鸭子类型与协议

> "如果它走起来像鸭子、叫起来像鸭子，那它就是鸭子。"

## 6.1 核心思想

Python 不在乎"对象是什么"，只在乎"对象能做什么"。

```python
def shout(obj):
    print(obj.upper())   # 不管 obj 是 str 还是 Duck，都行

shout("hello")   # "hello"
```

Java/C# 程序员会定义 `interface { String upper(); }` 然后让 `Duck implements Quackable`。Python：**直接调用**。

## 6.2 协议 = 隐式接口

一组相关方法的集合，叫"协议"（protocol）：

| 协议 | 方法 |
|---|---|
| 迭代协议 | `__iter__` |
| 序列协议 | `__len__`, `__getitem__` |
| 上下文协议 | `__enter__`, `__exit__` |
| 可调用协议 | `__call__` |
| 容器协议 | `__contains__`, `__len__` |
| 哈希协议 | `__hash__`, `__eq__` |

鸭子类型 = "对象实现了协议的方法 = 对象是协议的实例"。

## 6.3 EAFP vs LBYL

**EAFP**（Easier to Ask Forgiveness than Permission）：直接试，错了再处理。

**LBYL**（Look Before You Leap）：先检查再动手。

```python
# EAFP（Pythonic）
try:
    value = d[key]
except KeyError:
    value = default

# LBYL（非 Pythonic）
if key in d:
    value = d[key]
else:
    value = default
```

EAFP 在并发场景下更安全（检查到使用之间状态可能变）、通常更快（少一次查找）。

## 6.4 `collections.abc`：内置协议

判断一个对象是否实现某协议：

```python
from collections.abc import Iterable, Sequence, Mapping, Container, Sized

isinstance([], Iterable)         # True
isinstance([], Sequence)         # True
isinstance({}, Mapping)          # True
isinstance("abc", Sequence)      # True
isinstance(42, Iterable)         # False
```

自己实现协议时可以**显式继承** ABC（如 `class MyList(Sequence)`），会强制你实现所有方法。阶段 3 详讲。

## 6.5 结构化子类型：`typing.Protocol`

继承 `Protocol` 不要求 `is-a`，只要"形状一致"：

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

close_all([File(), Connection()])   # OK
```

`File` 没继承 `SupportsClose`，但因形状匹配，**mypy 会接受**。

阶段 3 详讲 `Protocol` 与 ABC 的取舍。

## 6.6 实战：解耦而非继承

```python
# 反例：继承 = 强耦合
class JSONExporter(BaseExporter):
    pass

# 正例：协议 = 弱耦合
class Exporter(Protocol):
    def export(self, data: dict) -> str: ...

class JSONExporter:
    def export(self, data: dict) -> str:
        return json.dumps(data)

class CSVExporter:
    def export(self, data: list[dict]) -> str: ...
    # 签名不匹配？mypy 会标黄，提示你修正接口
```

## 6.7 何时打破鸭子类型

鸭子类型不是银弹：

- **关键边界**（API 输入/输出、库接口）用 `Protocol` 加类型提示
- **核心业务** 用单元测试断言行为
- **运行时**用 `isinstance` / `hasattr` 做安全检查

```python
def serialize(obj) -> str:
    if hasattr(obj, "to_dict"):
        return json.dumps(obj.to_dict())
    raise TypeError(f"cannot serialize {type(obj).__name__}")
```

## 6.8 `typing` 里的协议

`typing` 自带一批常用协议：

```python
from typing import (
    Iterable, Iterator, Sequence, Mapping, MutableMapping,
    Set, Container, Sized, Hashable,
    Reversible, SupportsAbs, SupportsRound, SupportsInt, SupportsFloat,
    Callable, ContextManager,
)
```

阶段 4 系统讲 `typing`。

## 6.9 总结

| 你想要的 | 用 |
|---|---|
| 运行时多态 | 鸭子类型 + 单元测试 |
| 静态检查多态 | `typing.Protocol` |
| 强制实现接口 | `collections.abc` |
| 运行时安全检查 | `isinstance` / `hasattr` |
| 文档/可读 | 协议（隐式 + 显式） |

## 6.10 案例：阶段 2 项目怎么用协议

流式日志分析器：

- `Parser`：实现 `parse(line: str) -> Record` 协议
- `Analyzer`：实现 `analyze(records: Iterable[Record]) -> Stats` 协议
- `Renderer`：实现 `render(stats: Stats) -> str` 协议

每个组件可独立替换、新增，无需继承。测试也只测单组件。
