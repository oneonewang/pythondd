# 05 - `functools` 必知

`functools` 是函数式工具集。本节挑 5 个最常用的，足够覆盖 90% 场景。

## 5.1 `lru_cache` / `cache`：记忆化

```python
from functools import lru_cache, cache

@cache                # 3.9+，无限制
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

fib(100)              # 瞬间返回
```

```python
@lru_cache(maxsize=128)    # 限制最近 128 次调用
def slow_func(x, y):
    ...
```

**陷阱**：

1. **参数必须可哈希**（`list` / `dict` 不行，要转 `tuple` / `frozenset`）
2. **全局状态**——`cache` 跨调用累积，测试要清
3. **不要缓存生成器 / lambda**

```python
fib.cache_clear()           # 手动清空
```

## 5.2 `partial`：参数绑定

```python
from functools import partial

def power(base: float, exp: float) -> float:
    return base ** exp

square = partial(power, exp=2)        # 绑定 exp
square(5)                             # 25

cube = partial(power, exp=3)
cube(2)                               # 8
```

等价于：

```python
def square(base): return power(base, exp=2)
```

`partial` 保留 `__name__` / `__doc__`，比 lambda 友好。

## 5.3 `reduce`：累积

```python
from functools import reduce
import operator

reduce(operator.add, [1, 2, 3, 4])        # 10
reduce(operator.mul, [1, 2, 3, 4])        # 24
reduce(operator.concat, ["a", "b", "c"])  # "abc"
```

**用 reduce 还是循环**：能换成 `sum` / `math.prod` / 推导式就别用 reduce。

```python
# reduce 不可读
total = reduce(operator.add, xs, 0)

# sum 更好
total = sum(xs)
```

## 5.4 `singledispatch`：按类型分派

```python
from functools import singledispatch

@singledispatch
def serialize(obj) -> str:
    raise NotImplementedError(f"cannot serialize {type(obj)}")

@serialize.register
def _(obj: int) -> str:
    return str(obj)

@serialize.register
def _(obj: str) -> str:
    return f'"{obj}"'

@serialize.register
def _(obj: list) -> str:
    return "[" + ", ".join(serialize(x) for x in obj) + "]"

serialize(42)               # "42"
serialize("hi")             # '"hi"'
serialize([1, "x"])         # '[1, "x"]'
```

**继承也工作**：

```python
class MyInt(int): pass
serialize(MyInt(5))         # "5"   自动匹配 int
```

**注意**：被装饰的函数名不重要（`def _(obj: int)`），关键是参数类型注解。

`singledispatchmethod` 是对应的方法版本。

## 5.5 `cached_property`：计算属性

```python
from functools import cached_property

class DataSet:
    def __init__(self, raw: list[int]):
        self.raw = raw

    @cached_property
    def mean(self) -> float:
        print("computing mean...")
        return sum(self.raw) / len(self.raw)

    @cached_property
    def max(self) -> int:
        return max(self.raw)

ds = DataSet([1, 2, 3, 4])
ds.mean       # 第一次：computing mean... → 2.5
ds.mean       # 第二次：直接返回缓存
ds.max        # 第一次计算
```

**要点**：

- 第一次访问才计算
- 结果存到 `ds.__dict__["mean"]`
- 改 `raw` 不会让缓存失效
- `del ds.mean` 可清除

**替代 `@property` 的场景**：
- 计算昂贵
- 可能根本用不到
- 不希望每次访问都重算

## 5.6 `total_ordering`：少写几个比较

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, s: str):
        self.parts = tuple(int(x) for x in s.split("."))

    def __eq__(self, other): return self.parts == other.parts
    def __lt__(self, other): return self.parts < other.parts

Version("1.5") < Version("2.0")
Version("1.5") <= Version("2.0")
Version("1.5") != Version("2.0")
```

有了 `__eq__` 和 `__lt__`，`<=` / `>` / `>=` 自动可用。

## 5.7 `wraps`：保留原函数元信息

阶段 2 已学。`@wraps(func)` 复制 `__name__` / `__doc__` / `__module__`。

## 5.8 `cmp_to_key`：把老式比较函数转 key

```python
from functools import cmp_to_key

# sorted 支持 key=，不支持 cmp=
sorted(["aaa", "b", "cc"], key=cmp_to_key(lambda a, b: len(a) - len(b)))
# ["b", "cc", "aaa"]
```

## 5.9 选型速查

| 需求 | 用 |
|---|---|
| 缓存计算 | `@cache` / `@lru_cache` |
| 绑定部分参数 | `partial` |
| 序列累积 | `reduce`（少用） |
| 按类型分派 | `singledispatch` |
| 懒计算属性 | `cached_property` |
| 比较运算 | `total_ordering` |
| 装饰器保元 | `@wraps` |
