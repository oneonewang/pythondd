# 06 - 多继承与 Mixin

## 6.1 多继承基础

```python
class A:
    def m(self): return "A"

class B:
    def m(self): return "B"

class C(A, B):       # 先 A 后 B
    pass

C().m()              # "A"   按 MRO：A → B → object
```

## 6.2 菱形继承

```
       Animal
       /    \
      Dog    Bird
       \    /
        WorkingDog
```

```python
class Animal:
    def speak(self): return "..."

class Dog(Animal):
    def speak(self): return "Woof"

class Bird(Animal):
    def speak(self): return "Chirp"

class WorkingDog(Dog, Bird):
    pass

WorkingDog().speak()       # "Woof"   来自 Dog
WorkingDog.__mro__
# [WorkingDog, Dog, Animal, Bird, object]
```

**C3 线性化保证**：每个祖先只出现一次，且保持声明顺序。

## 6.3 Mixin 模式

Mixin = "提供一种能力的小类"，**不**用于独立实例化。

```python
class JsonMixin:
    def to_json(self) -> str:
        import json
        return json.dumps(self.__dict__)

class EqMixin:
    def __eq__(self, other): return self.__dict__ == other.__dict__
    def __hash__(self): return hash(tuple(sorted(self.__dict__.items())))

class User(JsonMixin, EqMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

u = User("alice", 30)
u.to_json()          # '{"name": "alice", "age": 30}'
```

**约定**：

- Mixin 类名以 `Mixin` 结尾
- 放在继承列表的**前面**（按优先级）
- 不调用 `super().__init__()`（除非有协作链）

## 6.4 协作多继承（`super()` 链）

让所有类都用 `super()`，形成"调用链"：

```python
class Base:
    def __init__(self):
        print("Base")
        super().__init__()

class A(Base):
    def __init__(self):
        print("A")
        super().__init__()

class B(Base):
    def __init__(self):
        print("B")
        super().__init__()

class C(A, B):
    def __init__(self):
        print("C")
        super().__init__()

C()
# C
# A
# B
# Base
```

`super()` 沿 MRO 找下一个，所以 C → A → B → Base。

**这叫"协作式多继承"**：每个类负责自己的一小段，调用链穿过所有合作者。

## 6.5 经典模式：序列化 / 比较 / 哈希 Mixin

```python
class ComparableMixin:
    def __lt__(self, other): return NotImplemented
    def __le__(self, other): return NotImplemented
    # ...

# Django ORM、SQLAlchemy、Django REST framework 大量使用
```

## 6.6 实战：可观察对象 Mixin

```python
class ObservableMixin:
    def __init__(self, *args, **kwargs):
        self._observers = []
        super().__init__(*args, **kwargs)

    def subscribe(self, callback):
        self._observers.append(callback)

    def notify(self, event):
        for cb in self._observers:
            cb(event)

class Counter(ObservableMixin):
    def __init__(self):
        super().__init__()
        self.n = 0

    def inc(self):
        self.n += 1
        self.notify({"event": "inc", "value": self.n})

c = Counter()
c.subscribe(lambda e: print(f"event: {e}"))
c.inc()
# event: {'event': 'inc', 'value': 1}
```

## 6.7 Mixin vs 装饰器

| | Mixin | 装饰器 |
|---|---|---|
| 形式 | 继承 | 函数包装 |
| 行为获取时机 | 类定义时 | 装饰时 |
| 能否访问 self/cls | 是 | 通过 wrapper |
| 能否影响 MRO | 是 | 否 |
| 适合 | 多个方法需要组合 | 单点拦截（计时、日志） |

阶段 2 装饰器 + 阶段 3 Mixin = 组合的两种正交工具。

## 6.8 真实例子：Django Class-Based Views

```python
class ProcessFormMixin:
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

class LoginView(ProcessFormMixin, TemplateView):
    def form_valid(self, form):
        # ...
        return redirect("home")
```

## 6.9 不要乱用多继承

**反模式**：

```python
class DatabaseMixin: ...     # 假装"通用"，实则绑死
class HttpMixin: ...
class User(DatabaseMixin, HttpMixin, JsonMixin, EqMixin, ...): pass
```

继承层数超过 3–4 层、Mixin 超过 4–5 个，**99% 是设计问题**。

**替代方案**：

- 组合（has-a 替代 is-a）
- 装饰器
- 中间件 / 拦截器

## 6.10 多继承检查清单

1. 是否有真正的菱形？ → 用 `__mro__` 验证
2. 所有 `__init__` 都调 `super().__init__()` 吗？ → 否则 MRO 链断
3. Mixin 命名以 `Mixin` 结尾
4. Mixin 放在继承列表前面
5. 不在 Mixin 里调 `super().__init__()`（除非真的需要）

## 6.11 Metaclass（点到为止）

`type` 是默认 metaclass。`metaclass=ABCMeta` 让 ABC 工作。**真实项目里几乎不会自己写 metaclass**——除非你在做框架。

```python
class MyMeta(type):
    def __new__(mcs, name, bases, namespace):
        # 可以做：注册类、自动加方法、强制接口
        return super().__new__(mcs, name, bases, namespace)

class MyClass(metaclass=MyMeta):
    pass
```

`__init_subclass__` 是 metaclass 90% 用例的更轻替代。
