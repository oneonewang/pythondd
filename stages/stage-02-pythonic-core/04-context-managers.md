# 04 - 上下文管理器

`with` 关键字让"获取资源"和"释放资源"在语法上配对，防止泄漏。

## 4.1 形式

```python
with EXPRESSION as VAR:
    BODY
```

等价于：

```python
mgr = EXPRESSION
VAR = mgr.__enter__()
try:
    BODY
finally:
    mgr.__exit__(exc_type, exc_val, tb)
```

任何实现 `__enter__` / `__exit__` 的对象都能用 `with`。

## 4.2 自己写一个

```python
class Timer:
    def __enter__(self):
        import time
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, tb):
        import time
        self.elapsed = time.perf_counter() - self._start
        return False   # 不吞异常

with Timer() as t:
    sum(range(10_000_000))
print(t.elapsed)
```

`__exit__` 返回 `True` 会吞掉异常（一般**不要**这样做）。

## 4.3 `@contextmanager` 把生成器变上下文

不用写类的"快捷方式"：

```python
from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.perf_counter()
    yield                       # __enter__ 之前在 yield 之前
    elapsed = time.perf_counter() - start
    print(f"elapsed: {elapsed:.3f}s")

with timer():
    sum(range(10_000_000))
```

`yield` 的值绑定到 `as VAR`。异常会传进生成器（`yield` 抛），所以你可以处理：

```python
@contextmanager
def catching_errors():
    try:
        yield
    except ValueError as e:
        print(f"caught: {e}")
        # 不 reraise，吞掉
```

## 4.4 `contextlib` 其他工具

### `closing`

把"有 `.close()` 但不是上下文管理器"的对象包装成上下文管理器。

### `suppress`

吞掉指定异常：

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    Path("missing.txt").unlink()
```

### `ExitStack`

动态管理多个上下文（数量运行时才知道）：

```python
from contextlib import ExitStack

files = [open(p) for p in paths]
with ExitStack() as stack:
    for f in files:
        stack.enter_context(f)  # 异常时反向 close
    # 任意一个出错，其余会自动关闭
```

### `nullcontext`

占位用。`if/else` 一边有 `with`、一边没有时的统一写法：

```python
from contextlib import nullcontext

if verbose:
    cm = open(log_path, "w")
else:
    cm = nullcontext()          # no-op

with cm as f:
    ...
```

## 4.5 真实场景

| 场景 | 实现 |
|---|---|
| 锁 | `with lock:`（`threading.Lock` 已实现） |
| 数据库事务 | `with session.begin():` |
| 临时目录 | `with TemporaryDirectory():` |
| 修改 cwd | `with chdir("/tmp"):`（自己写） |
| 抑制异常 | `with suppress(...):` |
| 重定向 stdout | `contextlib.redirect_stdout` |
| 计算耗时 | 自己写 / `time.perf_counter` |
| 资源池借/还 | 业务自写 |

## 4.6 临时目录 / 文件

```python
from tempfile import TemporaryDirectory, NamedTemporaryFile

with TemporaryDirectory() as tmpdir:
    p = Path(tmpdir) / "out.json"
    p.write_text("...")

# pytest 的 tmp_path fixture 就是基于 TemporaryDirectory
```

## 4.7 `__enter__` 返回什么

```python
class DB:
    def __enter__(self):
        self.conn = connect()
        return self.conn    # 用 as var 拿到的就是这个
```

不一定要 `return self`，可以 `return self.conn`，让 `with db as conn:` 写起来更顺。

## 4.8 异步上下文管理器（`async with`）

```python
class AsyncDB:
    async def __aenter__(self):
        self.conn = await connect()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, tb):
        await self.conn.close()
```

`@asynccontextmanager` 是异步版的 `contextmanager`。阶段 5 详讲。
