# 04 - 函数

## 4.1 定义与调用

```python
def add(a, b):
    return a + b

add(1, 2)        # 3
add(a=1, b=2)    # 关键字参数
```

## 4.2 默认参数

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"

greet("Alice")             # "Hello, Alice"
greet("Alice", "Hi")       # "Hi, Alice"
greet("Alice", greeting="Hi")
```

**默认参数只在函数定义时求值一次**。绝不要把可变对象当默认参数：

```python
# 错
def f(items=[]):
    items.append(1)
    return items

# 对
def f(items=None):
    if items is None:
        items = []
    items.append(1)
    return items
```

## 4.3 位置 vs 关键字

```python
def connect(host, port=80, timeout=10, use_tls=False):
    ...

connect("localhost")                              # 位置
connect("localhost", 8080)                         # 位置
connect("localhost", port=8080)                    # 关键字
connect("localhost", 8080, use_tls=True)           # 混用：位置必须在前
connect("localhost", timeout=5, port=443)         # 关键字顺序无所谓
```

## 4.4 *args 与 **kwargs

打包任意多的位置参数 / 关键字参数：

```python
def log(*args, **kwargs):
    print(args)    # tuple
    print(kwargs)  # dict

log(1, 2, 3, name="alice", age=30)
# (1, 2, 3)
# {'name': 'alice', 'age': 30}
```

**解包**（调用时）：

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
add(*nums)               # 等价 add(1, 2, 3)

opts = {"sep": ", ", "end": "!"}
print(*["a", "b", "c"], **opts)   # a, b, c!
```

**参数顺序约定**：

```python
def f(positional, *args, keyword_only, **kwargs):
    ...
```

`*args` 之后的参数必须用关键字传：

```python
def f(name, *, upper=False):
    return name.upper() if upper else name

f("alice")              # OK
f("alice", upper=True)  # OK
f("alice", True)        # 错
```

## 4.5 返回值

- 没有 `return` 时返回 `None`
- 可以返回多个值（其实是返回 tuple）

```python
def min_max(xs):
    return min(xs), max(xs)

lo, hi = min_max([3, 1, 2])   # 解包
```

## 4.6 作用域（LEGB）

Python 作用域查找顺序：**L**ocal → **E**nclosing → **G**lobal → **B**uilt-in

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)
    inner()       # local
    print(x)      # enclosing

outer()           # local / enclosing
print(x)          # global
```

`global` / `nonlocal` 用于在内部作用域修改外层变量，**尽量少用**：

```python
counter = 0
def inc():
    global counter
    counter += 1
```

> 经验：能传参就传参，能返回就返回，避免用 `global`。

## 4.7 一等公民

函数是对象，可以：

```python
# 1. 赋给变量
f = print
f("hi")              # hi

# 2. 放进容器
funcs = [str.lower, str.upper]
[f("Hello") for f in funcs]   # ['hello', 'HELLO']

# 3. 当参数（高阶函数）
sorted(["a", "B", "c"], key=str.lower)   # ['a', 'B', 'c']

# 4. 当返回值（闭包）
def make_adder(n):
    def add(x):
        return x + n
    return add

add5 = make_adder(5)
add5(3)      # 8
```

## 4.8 lambda — 匿名函数

只在赋值给变量或当参数时用，**不要**起名字。

```python
sorted(items, key=lambda x: x.priority)
```

> 反例：
> ```python
> # 错
> f = lambda x: x * 2
>
> # 对
> def f(x):
>     return x * 2
> ```

## 4.9 类型提示（阶段 4 详讲）

阶段 1 简单用一下，让自己习惯看：

```python
def add(a: int, b: int) -> int:
    return a + b
```

阶段 4 会讲 `Optional`、`Union`、`Generic`、`Protocol` 等高级用法。
