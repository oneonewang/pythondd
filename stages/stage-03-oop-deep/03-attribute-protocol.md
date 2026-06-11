# 03 - 属性访问协议

Python 读 / 写 / 删一个属性，背后是一串 `__getattr__` / `__setattr__` 等魔术方法。本节讲它们的精确行为，避免"循环调用"陷阱。

## 3.1 属性查找的完整顺序

读 `obj.attr`：

1. 调用 `type(obj).__getattribute__(obj, 'attr')`（默认实现）
2. 默认实现按顺序找：
   - 类的数据描述符（`__get__` + `__set__`/`__delete__`）
   - 实例字典 `obj.__dict__`
   - 类的非数据描述符（只有 `__get__`）
   - 类的普通方法
3. 都没找到 → 抛 `AttributeError`
4. `AttributeError` 触发 `type(obj).__getattr__(obj, 'attr')`
5. 还找不到 → 抛 `AttributeError`

## 3.2 `__getattr__` vs `__getattribute__`

| | `__getattribute__` | `__getattr__` |
|---|---|---|
| 何时调用 | **每次**属性访问 | 普通查找失败时 |
| 默认行为 | 实现查找逻辑 | 抛 `AttributeError` |

```python
class Trace:
    def __getattribute__(self, name):
        print(f"GET {name}")
        return super().__getattribute__(name)

    def __getattr__(self, name):
        print(f"MISS {name}")
        raise AttributeError(name)

t = Trace()
t.x = 1
t.x              # GET x
t.y              # GET y  →  MISS y  →  AttributeError
```

**大多数情况只需要 `__getattr__`**，用来兜底不存在的属性。

## 3.3 代理模式（最常用）

把属性访问转发给内部对象：

```python
class Proxy:
    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        # 只在 self.__dict__ 里找不到时才调用
        return getattr(self._target, name)

# 用法
class User:
    name = "alice"
    age = 30

p = Proxy(User())
p.name              # "alice"   来自 _target
p.age               # 30
p.unknown           # AttributeError
```

**关键**：`__getattr__` 只在属性**找不到**时调用，**不会**陷入无限递归——因为 `self._target` 是真实赋值进 `__dict__` 的，正常查找能拿到。

## 3.4 `__setattr__`：拦截赋值

```python
class Strict:
    def __setattr__(self, name, value):
        if not name.isupper():
            raise AttributeError(f"attribute must be UPPERCASE, got {name!r}")
        super().__setattr__(name, value)

s = Strict()
s.NAME = "ok"      # OK
s.name = "no"      # AttributeError
```

**坑**：

```python
class Bad:
    def __setattr__(self, name, value):
        self.name = value        # 死循环！__setattr__ 又调到自己

# 对
class Bad:
    def __setattr__(self, name, value):
        super().__setattr__(name, value)   # 委托给 object
```

`__init__` 中 `self.x = ...` 也会触发 `__setattr__`——所以通常需要先把"受保护"的属性绕过它。

## 3.5 验证模式

```python
class Validated:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __setattr__(self, name, value):
        if name == "age" and (value < 0 or value > 150):
            raise ValueError("age out of range")
        super().__setattr__(name, value)

v = Validated(age=30)    # OK
v.age = 200              # ValueError
```

## 3.6 `__delattr__`

```python
class Locked:
    def __delattr__(self, name):
        raise AttributeError(f"cannot delete {name!r}")

class C:
    x = Locked()

c = C()
del c.x              # AttributeError
```

`__init__` 期间不要在 `__delattr__` 里访问 `__dict__`，会循环。

## 3.7 `__dir__`

`dir(obj)` 的来源：

```python
class Show:
    def __dir__(self):
        return ["alpha", "beta", "gamma"]

dir(Show())        # ['alpha', 'beta', 'gamma']
```

阶段 2 的 `Indenter` 没必要重写——内置已经够好。

## 3.8 `__slots__` 与属性协议（连接下一节）

```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

加了 `__slots__` 后：

- 实例**没有 `__dict__`**（节省内存）
- 不能再加 `__slots__` 之外的属性
- 属性查找直接走 slot descriptor（更快）

## 3.9 综合实战：ORM 风格的字段

```python
class Field:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"_{name}"

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return getattr(obj, self.storage_name)

    def __set__(self, obj, value):
        setattr(obj, self.storage_name, value)

class User:
    name = Field()
    age = Field()

    def __init__(self, name, age):
        self.name = name
        self.age = age

u = User("alice", 30)
u.name         # "alice"
u._name        # AttributeError   真正存在的是 _name
```

## 3.10 调试技巧

```python
# 看属性查找链
type(obj).__mro__              # 类链
obj.__dict__                   # 实例属性
vars(obj) == obj.__dict__      # True
dir(obj)                       # 所有可见属性
hasattr(obj, 'x')              # 不会抛异常

# 找描述符
inspect.getattr_static(obj, 'x')   # 绕过 __getattr__/__getattribute__
```

`inspect.getattr_static` 调试属性查找冲突时非常有用——阶段 6 详讲。
