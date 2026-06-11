# 02 - 描述符（Descriptor）

描述符是 Python 对象模型的基石。理解它，你就理解了 `property`、方法绑定、`classmethod`、`staticmethod` 在做什么。

## 2.1 描述符协议

实现下面任一方法的对象就是描述符：

| 方法 | 签名 | 角色 |
|---|---|---|
| `__get__` | `(self, obj, type=None) -> Any` | 取值时 |
| `__set__` | `(self, obj, value) -> None` | 赋值时 |
| `__delete__` | `(self, obj) -> None` | `del` 时 |
| `__set_name__` | `(self, owner, name) -> None` | 3.6+，描述符绑定到类属性时调用一次 |

```python
class Ten:
    """最简单的描述符：忽略 obj、value，永远返回 10。"""
    def __get__(self, obj, type=None):
        return 10

class C:
    x = Ten()       # 描述符作为类属性

c = C()
c.x               # 10
C.x               # 10  （type 不为 None 时）
```

## 2.2 数据描述符 vs 非数据描述符

- **数据描述符**：定义了 `__get__` **和** `__set__` / `__delete__`
- **非数据描述符**：只定义了 `__get__`

**关键规则**：数据描述符 > 实例字典 > 非数据描述符。

```python
class Validated:
    def __get__(self, obj, type=None):
        return obj._x              # 从实例的 _x 取
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("must be >= 0")
        obj._x = value             # 存到实例的 _x

class C:
    x = Validated()                # 数据描述符

c = C()
c.x = 10                          # OK
c._x                              # 10
c.x                               # 10
c.x = -1                          # ValueError

c.x = 999                         # 再设一次
c.x = 5                           # OK，覆盖 _x
```

**为什么这样设计**：让 `property` 之类能在赋值时校验、不让实例字典意外覆盖。

## 2.3 自己写一个 `property`

```python
class MyProperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return self.fget(obj)

class C:
    @MyProperty
    def name(self):
        return self._name
```

简单版 `property` ≈ 一个数据描述符（`__get__`）。

## 2.4 `property` 完整实现

```python
class MyProperty:
    def __init__(self, fget=None, fset=None, fdel=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("not readable")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("not writable")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("not deletable")
        self.fdel(obj)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel)
```

## 2.5 方法是什么？

```python
class C:
    def m(self):
        return self

c = C()
c.m               # <bound method C.m of ...>
C.m               # <function C.m at ...>
```

**方法是非数据描述符**：只定义了 `__get__`。`c.m` 触发了"绑定"——返回一个 partial 应用 `c` 的 callable。

```python
# 等价
c.m()             # c.m(self=c)
C.m(c)            # C.m(self=c)
```

**在 CPython 字节码层**：

```python
class function:
    def __get__(self, obj, type=None):
        if obj is None:
            return self
        from types import MethodType
        return MethodType(self, obj)
```

所以 `c.m` 是 `function.__get__(m, c, C)` 的结果。

## 2.6 `classmethod` / `staticmethod` 真相

```python
class C:
    @classmethod
    def cm(cls):
        return cls

    @staticmethod
    def sm():
        return "sm"
```

两者都是描述符：

| 装饰器 | 行为 |
|---|---|
| `@staticmethod` | `__get__` 返回自身（不绑定） |
| `@classmethod` | `__get__` 返回 `MethodType(func, cls)`（绑定 cls） |

```python
C.cm()            # <class '__main__.C'>
C.sm()            # "sm"
c = C()
c.cm()            # <class '__main__.C'>  仍然绑 cls
c.sm()            # "sm"   不绑 self
```

**对比**：

| | 实例方法 | `classmethod` | `staticmethod` |
|---|---|---|---|
| 拿到 self/cls? | self | cls | 都没有 |
| 子类调用时 | self 是子类实例 | cls 是子类 | 不变 |
| 用途 | 业务逻辑 | 替代构造、工厂 | 工具函数 |

```python
# classmethod 经典用法：替代构造
class Date:
    def __init__(self, y, m, d):
        self.y, self.m, self.d = y, m, d

    @classmethod
    def from_string(cls, s):
        y, m, d = s.split("-")
        return cls(int(y), int(m), int(d))

Date.from_string("2024-01-15")
```

## 2.7 `__set_name__`（3.6+）

描述符绑定到类属性时自动调用，可以拿到 owner 和 属性名：

```python
class Logged:
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, type=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        print(f"set {self.name} = {value!r}")
        setattr(obj, self.private_name, value)

class C:
    x = Logged()

c = C()
c.x = 42         # set x = 42
c.x              # 42
```

不用写 `_x` 这种魔法名字——描述符自己存到 `_<self.name>`。

## 2.8 实战：验证器

```python
class Validated:
    def __init__(self, *, min=None, max=None):
        self.min = min
        self.max = max

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, type=None):
        return getattr(obj, f"_{self.name}")

    def __set__(self, obj, value):
        if self.min is not None and value < self.min:
            raise ValueError(f"{self.name} must be >= {self.min}")
        if self.max is not None and value > self.max:
            raise ValueError(f"{self.name} must be <= {self.max}")
        setattr(obj, f"_{self.name}", value)

class Person:
    age = Validated(min=0, max=150)
    name = Validated()

p = Person()
p.age = 30       # OK
p.age = 200      # ValueError
```

## 2.9 性能注意

描述符每次访问都触发 `__get__`，简单场景下比普通属性慢。

但在 ORM、序列化、验证等场景，描述符的"集中拦截"价值远大于开销。

## 2.10 总结

- 描述符 = 实现 `__get__` / `__set__` / `__delete__` 的对象
- `property` / 方法 / `classmethod` / `staticmethod` 都是描述符
- 数据描述符 > 实例字典 > 非数据描述符
- `__set_name__` 让描述符知道自己叫什么（3.6+）
