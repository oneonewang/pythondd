# 03 - 装饰器

装饰器 = "在不动原函数的前提下，给它加新能力"。本质是**接收函数、返回函数的可调用对象**。

## 3.1 最简单的装饰器

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"hi {name}")

greet("alice")
# before
# hi alice
# after
```

**等价于**：

```python
greet = my_decorator(greet)
```

## 3.2 `functools.wraps`：保留元信息

不写 `wraps` 会丢函数名、文档、签名：

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)   # 把 func 的 __name__/__doc__/__module__ 复制给 wrapper
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

> **永远加 `@wraps`**。否则 `help(greet)` 会显示 `wrapper()`，调试地狱。

## 3.3 计时装饰器

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper
```

## 3.4 日志装饰器

```python
def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"call {func.__name__}{args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"-> {result!r}")
        return result
    return wrapper
```

## 3.5 带参数的装饰器

把外层函数再加一层（"装饰器工厂"）：

```python
def repeat(times: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def hello():
    print("hi")
```

## 3.6 装饰链：从下往上应用

```python
@timer
@log_calls
@repeat(3)
def work():
    ...
```

执行顺序：`work = timer(log_calls(repeat(3)(work)))`，运行时**外层先入、内层先执行**：

```python
# 等价
work()  # 顺序：timer 头 -> log_calls 头 -> repeat 循环 3 次 work -> log_calls 尾 -> timer 尾
```

## 3.7 类装饰器

有时装饰器需要状态：

```python
class CountCalls:
    def __init__(self, func):
        wraps(func)(self)   # 让 self 也保留 func 的元信息
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

@CountCalls
def hello():
    print("hi")

hello()
hello()
print(hello.count)   # 2
```

## 3.8 内置常用装饰器

```python
# 静态方法、类方法
class A:
    @staticmethod
    def f(): ...

    @classmethod
    def g(cls): ...

# 属性
class B:
    @property
    def x(self): ...

# functools
from functools import lru_cache, cache

@cache                # 3.9+ 等价 lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

## 3.9 装饰类

反过来——装饰器也能修改/替换类：

```python
def add_repr(cls):
    if "__repr__" not in cls.__dict__:
        cls.__repr__ = lambda self: f"{cls.__name__}({self.__dict__})"
    return cls

@add_repr
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

框架（dataclass、attrs、SQLAlchemy）都这么干。

## 3.10 常见坑

1. **忘记 `wraps`** → `help()`、调试器、单元测试全废。
2. **副作用**：装饰器只在 import 时执行一次，计时统计会跨调用累积。
3. **类型签名变化**：`@wraps` 不会复制签名。需要 `typing.ParamSpec`（阶段 4 详讲）才能精确标注。
4. **不可哈希**：装饰类时 `wraps` 复制元信息的方法学（`wraps` 用的是 `__dict__` 更新，所以被装饰类依然可哈希，除非你改了 `__hash__`）。

## 3.11 用 `inspect` 检查

```python
import inspect
inspect.signature(work)              # 参数签名
inspect.getsource(work)              # 源码
inspect.iscoroutinefunction(work)    # 是否 async
```
