# 02 - 语法基础：与其他语言的差异

> 假设你已经会 Java / C++ / Go / JS 中至少一种。本节只讲 Python 的"不同"。

## 2.1 缩进 = 语法

Python 用缩进表示代码块（4 空格，不要用 Tab）：

```python
# Python
def foo(x):
    if x > 0:
        return x
    return 0
```

```java
// Java 等价写法
int foo(int x) {
    if (x > 0) {
        return x;
    }
    return 0;
}
```

> 经验：让 ruff 自动格式化（`uv run ruff format .`），永远不要手抖改缩进。

## 2.2 动态类型 + 强类型

```python
x = 1          # int
x = "hello"    # str，类型可变
x = [1, 2, 3]  # list
```

但**强类型**：不同类型不会自动转换。

```python
1 + "2"     # TypeError: unsupported operand type(s)
"1" + 2     # TypeError（不像 JS 那样 "12"）
```

需要显式转换：

```python
str(1) + "2"   # "12"
int("1") + 2   # 3
```

> 风格：变量赋值不要写类型注解，类型提示写在函数签名上（阶段 4 详讲）。

```python
# 反例
x: int = 1

# 正例
x = 1

def add(a: int, b: int) -> int:
    return a + b
```

## 2.3 一切皆对象

数字、字符串、函数、类、模块都是对象，可以：

- 赋给变量
- 当参数传
- 当返回值
- 放进容器

```python
def shout(s: str) -> str:
    return s.upper()

f = shout                # 函数也是对象
print(f("hi"))           # "HI"
funcs = [str.lower, str.upper, str.title]
for fn in funcs:
    print(fn("hello"))   # hello / HELLO / Hello
```

## 2.4 字符串

Python 没有 char 类型，单字符就是长度为 1 的字符串。

三种字符串字面量：

```python
s1 = 'hello'
s2 = "hello"
s3 = """multi
line
string"""
```

**f-string**（3.6+，几乎总是用这个）：

```python
name = "world"
print(f"hello {name}")           # hello world
print(f"1 + 2 = {1 + 2}")        # 1 + 2 = 3
print(f"pi = {3.14159:.2f}")     # pi = 3.14
print(f"{'pad':>10}")            # 右侧 10 宽填充
```

> 反例：用 `%` 或 `.format()` 是老写法，新代码统一 f-string。

**不可变**：

```python
s = "hello"
s[0] = "H"   # TypeError
s = "H" + s[1:]  # 正确：创建新串
```

## 2.5 真值

以下都是 **假**（falsy）：

- `False` / `None`
- 任何数值类型的 `0`（`0`, `0.0`）
- 空容器：`""`, `[]`, `()`, `{}`, `set()`
- 自定义类型如果定义了 `__bool__` / `__len__` 也按这个规则

其他都真。

```python
# 习惯写法
items = []
if not items:
    print("empty")

# 不要这样写
if len(items) == 0:   # 非 Pythonic
    ...
```

## 2.6 控制流

```python
# if / elif / else（注意 elif 不是 else if）
if x > 0:
    ...
elif x < 0:
    ...
else:
    ...

# for 遍历任何可迭代对象
for item in collection:
    ...

# while
while condition:
    ...

# 没有 do-while，没有 switch（3.10 之前）。3.10+ 有 match-case
```

`match-case`（3.10+，阶段 4 详讲）：

```python
match command.split():
    case ["quit"]:
        ...
    case ["go", direction]:
        ...
    case _:
        ...
```

## 2.7 习惯用法速览

| 场景 | Pythonic 写法 | 反例 |
|---|---|---|
| 交换变量 | `a, b = b, a` | 用临时变量 |
| 链式比较 | `0 < x < 10` | `x > 0 and x < 10` |
| 枚举 | `for i, v in enumerate(items)` | `for i in range(len(items))` |
| 同时遍历 | `for k, v in d.items()` | 先 keys 再索引 |
| 跳过 / 中断 | `continue` / `break` | 用标志位 |
| 异常代替错误码 | 抛异常 | 返回 -1 / null |

## 2.8 注释

```python
# 单行注释

"""
多行字符串当文档用，不是注释。
放在模块/函数/类开头就是 docstring。
"""
```

docstring 有约定格式（Google / NumPy / Sphinx），阶段 6 详讲。
