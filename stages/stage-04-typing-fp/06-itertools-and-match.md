# 06 - `itertools` 必知 + 模式匹配

## 6.1 无限迭代器

```python
from itertools import count, cycle, repeat

count(10)               # 10, 11, 12, ...    无限
count(10, 2)            # 10, 12, 14, ...
cycle([1, 2, 3])        # 1, 2, 3, 1, 2, 3, ...    无限
repeat("x", 3)          # "x", "x", "x"
```

## 6.2 切片

```python
from itertools import islice, dropwhile, takewhile

islice(range(100), 5, 10)                # 5 6 7 8 9    替代 range(5, 10)
islice(range(100), 10)                   # 0..9
islice(range(100), 0, 10, 2)             # 0 2 4 6 8

dropwhile(lambda x: x < 5, [1, 3, 5, 7]) # 5 7     跳过前缀
takewhile(lambda x: x < 5, [1, 3, 5, 7]) # 1 3     取前缀
```

## 6.3 串联与展平

```python
from itertools import chain, chain.from_iterable

chain([1, 2], [3, 4])                # 1 2 3 4
chain.from_iterable([[1, 2], [3]])   # 1 2 3   展平一层
```

## 6.4 分组

```python
from itertools import groupby

# 数据必须按 key 排序
data = sorted([("a", 1), ("b", 2), ("a", 3), ("b", 4)], key=lambda x: x[0])
for key, group in groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# a [('a', 1), ('a', 3)]
# b [('b', 2), ('b', 4)]
```

## 6.5 笛卡尔积 / 排列 / 组合

```python
from itertools import product, permutations, combinations

list(product([1, 2], ["a", "b"]))
# [(1,'a'), (1,'b'), (2,'a'), (2,'b')]

list(permutations([1, 2, 3], 2))
# [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]

list(combinations([1, 2, 3, 4], 2))
# [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]
```

## 6.6 累加与配对

```python
from itertools import accumulate, pairwise

list(accumulate([1, 2, 3, 4]))            # [1, 3, 6, 10]
list(accumulate([1, 2, 3, 4], operator.mul))  # [1, 2, 6, 24]
list(pairwise([1, 2, 3, 4]))              # [(1,2), (2,3), (3,4)]
```

## 6.7 复制迭代器

```python
from itertools import tee

a, b = tee(range(5), 2)                # 两个独立迭代器
list(a)                                # 0 1 2 3 4
list(b)                                # 0 1 2 3 4
```

**注意**：会缓存，源迭代器大的话别用。

## 6.8 实战：流式分组

```python
def group_by_lazy(items, key):
    """按 key 排序并 groupby。注意：groupby 要求数据已按 key 排序。"""
    items_sorted = sorted(items, key=key)
    return ((k, list(g)) for k, g in groupby(items_sorted, key=key))
```

## 6.9 模式匹配 `match ... case`（3.10+）

阶段 1 简单提过，本节深入。

### 字面量

```python
match command:
    case "quit":
        ...
    case "go":
        ...
    case _:
        ...
```

### 序列

```python
match args:
    case []:
        print("no args")
    case [x]:
        print(f"one: {x}")
    case [x, y]:
        print(f"two: {x} {y}")
    case [x, *rest]:
        print(f"head: {x}, tail: {rest}")
```

**精确长度**用 `[]` / `[x]` / `[x, y]`；**任意长度**用 `[x, *rest]`。

### 映射

```python
match point:
    case {"x": x, "y": y}:
        print(f"({x}, {y})")
    case {"x": x, "y": y, "z": z}:
        print(f"3D: ({x}, {y}, {z})")
    case _:
        print("unknown")
```

### 类

```python
class Point:
    __match_args__ = ("x", "y")        # 3.10+ 声明位置参数名
    def __init__(self, x, y):
        self.x, self.y = x, y

match p:
    case Point(0, 0):
        print("origin")
    case Point(x, 0):
        print(f"on x-axis at {x}")
    case Point(x, y):
        print(f"({x}, {y})")
```

### OR 模式 + 守卫

```python
match value:
    case 0 | 1 | 2:                       # OR
        print("small")
    case n if n < 0:                      # guard
        print("negative")
    case n if n > 100:
        print("large")
```

### AS 绑定

```python
match point:
    case (x, y) as p:
        print(f"point {p} = ({x}, {y})")
```

### 实战：解析命令行

```python
def handle(args: list[str]) -> None:
    match args:
        case ["run", *files]:
            for f in files:
                run(f)
        case ["validate", file]:
            validate(file)
        case ["summary", file, "--json"]:
            summary(file, as_json=True)
        case ["--help"] | []:
            print(HELP)
        case _:
            print(f"unknown: {args}")
```

## 6.10 模式匹配 vs if/elif

| | `match` | `if/elif` |
|---|---|---|
| 结构化数据 | ✅ 强 | ❌ 弱 |
| 可读性 | 模式复杂时差 | 简单时好 |
| 性能 | 略快（CPython 优化） | 一般 |
| 反模式 | 简单比较用 match 反而绕 | 模式多时 if/elif 累 |

**经验**：超过 3 个分支 + 模式化数据用 match；简单相等比较用 if/elif。

## 6.11 速查

| 需求 | 用 |
|---|---|
| 无限计数 | `count` / `cycle` |
| 切片迭代器 | `islice` / `dropwhile` / `takewhile` |
| 串联 | `chain` |
| 分组（需排序） | `groupby` |
| 累加 | `accumulate` |
| 配对 | `pairwise`（3.10+） |
| 笛卡尔积 | `product` |
| 字面量分发 | `match` / `case` |
| 序列解构 | `match [x, *rest]` |
| 类解构 | `case Point(x, y)` |
