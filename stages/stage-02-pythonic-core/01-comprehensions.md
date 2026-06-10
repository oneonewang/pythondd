# 01 - 推导式

推导式是 Python 最常用的"惯用法"之一：用一行表达式代替 3–5 行累加循环。

## 1.1 list 推导式

```python
# 反例
squares = []
for x in range(10):
    squares.append(x * x)

# 正例
squares = [x * x for x in range(10)]
```

**带条件**：

```python
evens = [x for x in range(10) if x % 2 == 0]
```

**嵌套循环**：

```python
# 二维展开
flat = [x for row in matrix for x in row]

# 笛卡尔积
pairs = [(x, y) for x in xs for y in ys if x != y]
```

**带表达式**（不只是取值）：

```python
names = [u.name.strip().lower() for u in users if u.active]
```

## 1.2 dict 推导式

```python
# 反例
inv = {}
for k, v in original.items():
    inv[v] = k

# 正例
inv = {v: k for k, v in original.items()}

# 过滤
adults = {name: age for name, age in users.items() if age >= 18}
```

## 1.3 set 推导式

```python
lengths = {len(word) for word in words}
```

## 1.4 生成器表达式（终极武器）

把 `[]` 换成 `()` 就是生成器：

```python
# list —— 一次性把 1 亿个数装进内存
squares_list = [x * x for x in range(100_000_000)]

# generator —— 按需产出，零内存
squares_gen = (x * x for x in range(100_000_000))
sum(squares_gen)   # OK，占内存 O(1)
```

> 经验：
> - 只需要"遍历一次"用生成器
> - 需要多次遍历、取长度、按下标访问用 list
> - 体积小（<几千）用 list 没问题；体积大且一次性用 → 生成器

## 1.5 何时**不**用推导式

**判断标准**：单行能不能读懂。

```python
# OK：清晰
nums = [int(s) for s in strings if s.strip()]

# 不要这样：分支太多塞不下一行
# 拆成函数 / 用循环
result = [
    transform(x)
    for x in items
    if cond_a(x) and cond_b(x) and not cond_c(x)
    if x not in seen
]
```

**有副作用的循环**不要改成推导式：

```python
# 错
[cache.write(k, v) for k, v in data.items()]

# 对
for k, v in data.items():
    cache.write(k, v)
```

## 1.6 性能与可读性

推导式在 CPython 里是字节码优化的，通常比手写循环快 10–30%。

但**可读性优先**。如果推导式让你需要 5 秒才能看懂，就拆开。

## 1.7 walrus 运算符（3.8+）

`a := b` 在表达式内赋值。常用于推导式里避免重复计算：

```python
# 反例
results = [compute(x) for x in data if compute(x) is not None]

# 正例
results = [y for x in data if (y := compute(x)) is not None]
```

不要滥用。多数情况拆成普通循环更清楚。

## 1.8 常见模式速查

| 需求 | 写法 |
|---|---|
| 平方列表 | `[x*x for x in xs]` |
| 长度去重 | `{len(s) for s in strs}` |
| 反转字典 | `{v: k for k, v in d.items()}` |
| 索引 + 值 | `[(i, v) for i, v in enumerate(xs)]` |
| 同时遍历 | `[f(a, b) for a, b in zip(xs, ys)]` |
| 过滤 + 转换 | `[f(x) for x in xs if p(x)]` |
| 嵌套展平 | `[x for row in mat for x in row]` |
| 大数据 | `(x*x for x in range(10**8))` |
