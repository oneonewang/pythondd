# 02 - 迭代器与生成器

## 2.1 迭代器协议

任何实现了 `__iter__` / `__next__` 的对象都是迭代器：

```python
from collections.abc import Iterator, Iterable

# Iterable：可迭代（有 __iter__）
# Iterator：迭代器（有 __iter__ + __next__）

it = iter([1, 2, 3])        # list -> iterator
next(it)                      # 1
next(it)                      # 2
next(it)                      # 3
next(it)                      # StopIteration
```

`for x in xs` 实际做的事：

```python
it = iter(xs)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    # 循环体
```

## 2.2 自定义迭代器

```python
class Countdown:
    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> "Countdown":
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

for i in Countdown(3):
    print(i)   # 3 2 1
```

## 2.3 生成器：`yield` 简化迭代器

上面 5 行类 = 下面 2 行函数：

```python
def countdown(start: int):
    while start > 0:
        yield start
        start -= 1
```

`yield` 把函数变成"懒求值"工厂。调用函数不执行、返回一个生成器对象；每次 `next()` 执行到下一个 `yield`。

## 2.4 生成器表达式

```python
# 列表推导式：一次性算完
squares = [x * x for x in range(10)]

# 生成器表达式：按需产出
squares = (x * x for x in range(10))
```

## 2.5 何时用生成器

**任何"流式 / 一次遍历 / 不知道有多长"的场景**：

- 读大文件
- 数据库游标
- 网络分块下载
- 无限序列
- 数据管线

**反例**（不该用生成器）：

- 需要反复遍历
- 需要取长度、按下标
- 数据量小、生成器反而绕弯

## 2.6 `yield from`：委托子迭代器

```python
def chain(*iterables):
    for it in iterables:
        for x in it:        # 显式循环
            yield x

def chain(*iterables):
    for it in iterables:
        yield from it       # 委托（更快、可读性更好）
```

`yield from` 还会**透传** `send` / `throw` / `return` 值（阶段 3 详讲）。

## 2.7 双向通信：`send`

```python
def averager():
    total = 0.0
    count = 0
    avg = None
    while True:
        x = yield avg
        if x is None:
            break
        total += x
        count += 1
        avg = total / count
```

```python
gen = averager()
next(gen)             # 启动到第一个 yield，avg=None
gen.send(10)          # 0 -> 10.0
gen.send(20)          # 15.0
gen.send(None)        # 触发 break
```

> 阶段 2 不强求。生成器作协程是 `asyncio` 之前的并发方案，现已被 `asyncio` 取代。

## 2.8 实战：流式管线

```python
from pathlib import Path

def read_lines(path: Path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()

def filter_level(lines, level: str):
    for line in lines:
        if f" {level} " in line:
            yield line

def parse(lines):
    for line in lines:
        ts, level, msg = line.split(" ", 2)
        yield {"ts": ts, "level": level, "msg": msg}

# 管线
pipeline = parse(filter_level(read_lines(Path("app.log")), "ERROR"))
for record in pipeline:
    print(record)
```

**每一段都是生成器 → 整个管道 O(1) 内存**。

## 2.9 `itertools` 必知

```python
from itertools import (
    islice, chain, takewhile, dropwhile,
    groupby, tee, accumulate, product, permutations
)

# 切片（懒）
islice(range(100), 5, 10)         # 等价 range(5, 10)，但作用于任意迭代器

# 串联
chain([1, 2], [3, 4])             # 1 2 3 4

# 谓词切片
takewhile(lambda x: x < 5, [1, 3, 5, 7])  # 1 3
dropwhile(lambda x: x < 5, [1, 3, 5, 7])  # 5 7

# 分组（要求数据已按 key 排序！）
groupby(sorted(items, key=key), key=key)

# 累加
list(accumulate([1, 2, 3, 4]))     # [1, 3, 6, 10]
```

阶段 4 还会深入讲 `itertools`。

## 2.10 调试技巧

```python
def gen():
    yield 1
    yield 2
    yield 3

g = gen()
print(list(g))     # [1, 2, 3]
print(list(g))     # []   已耗尽！

# 想要反复遍历，把"已耗尽"作为"产出 0 次"对待。
# 重新调用 gen() 拿新对象。
```
