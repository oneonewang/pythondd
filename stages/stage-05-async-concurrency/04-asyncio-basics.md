# 04 - `asyncio` 基础

## 4.1 为什么 asyncio

- `threading` 每个线程 8 MB 起步，1000 个线程 = 8 GB
- `asyncio` 单线程、协程 KB 级，**成千上万并发**
- IO 等待时**切到其他任务**，不浪费 CPU
- 写起来像同步代码（`async` / `await`）

## 4.2 协程（coroutine）

```python
import asyncio

async def greet(name: str) -> str:
    await asyncio.sleep(0.1)       # 让出控制权
    return f"hello {name}"

# 调协程 = 返回 coroutine 对象
coro = greet("alice")
# 跑协程 = 拿到结果
result = asyncio.run(greet("alice"))    # "hello alice"
```

> 调 `async def` 返回的**不是值**，是协程对象。必须 await / run 才执行。

## 4.3 `await` 的本质

`await coro` 表示"我让出 CPU，等 `coro` 完成再继续"。事件循环会调度其他协程。

```python
async def main():
    # 顺序执行
    r1 = await greet("alice")     # 等 0.1s
    r2 = await greet("bob")       # 再等 0.1s
    # 总耗时 0.2s

    # 并发执行
    r1, r2 = await asyncio.gather(
        greet("alice"),
        greet("bob"),
    )
    # 总耗时 0.1s
```

## 4.4 `asyncio.gather`：并发多个协程

```python
async def fetch(url: str) -> str:
    await asyncio.sleep(0.1)
    return f"data from {url}"

async def main():
    urls = [f"http://api/{i}" for i in range(10)]
    results = await asyncio.gather(*[fetch(u) for u in urls])
    print(results)        # 10 个结果，0.1s 完成
```

`gather` 接收多个协程，**同时跑**，全部完成后返回 `list[结果]`。

**选项**：

```python
asyncio.gather(*coros, return_exceptions=True)   # 异常当结果返回
asyncio.gather(*coros, return_exceptions=False)  # 任何一个异常，整个 gather 失败
```

## 4.5 `asyncio.create_task`：手动调度

```python
async def main():
    t1 = asyncio.create_task(fetch("a"))
    t2 = asyncio.create_task(fetch("b"))
    # ... 干别的事 ...
    r1 = await t1
    r2 = await t2
```

`create_task` 把协程包成 `Task` 立即调度。**配合 `gather` 是常见组合**。

## 4.6 `asyncio.run` vs `await` vs `loop.create_task`

| 场景 | 用 |
|---|---|
| 顶层入口（main 函数） | `asyncio.run(coro())` |
| 在协程里启动并发 | `asyncio.gather(...)` / `asyncio.create_task(...)` |
| 后台 fire-and-forget | `asyncio.create_task(...)` |
| 手动管理 event loop | `asyncio.new_event_loop()`（少用） |

## 4.7 一个完整例子

```python
import asyncio
import time

async def say_after(delay: float, what: str) -> str:
    await asyncio.sleep(delay)
    return what

async def main():
    start = time.perf_counter()
    r1, r2, r3 = await asyncio.gather(
        say_after(1, "hello"),
        say_after(2, "world"),
        say_after(1.5, "!"),
    )
    print(r1, r2, r3)
    print(f"elapsed: {time.perf_counter() - start:.1f}s")   # 2.0s
```

## 4.8 `async for` 异步迭代器

```python
class AsyncRange:
    def __init__(self, n: int) -> None:
        self.n = n
        self.i = 0

    def __aiter__(self):
        return self

    async def __anext__(self) -> int:
        if self.i >= self.n:
            raise StopAsyncIteration
        self.i += 1
        await asyncio.sleep(0.01)
        return self.i - 1

async def main():
    async for i in AsyncRange(5):
        print(i)
```

## 4.9 `async with`：异步上下文管理器

```python
class AsyncConnection:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

async def main():
    async with AsyncConnection() as conn:
        await conn.query(...)
```

也可以用 `@asynccontextmanager` 装饰器（阶段 2 学过）：

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def timer():
    start = time.perf_counter()
    yield
    print(f"elapsed: {time.perf_counter() - start:.3f}s")
```

## 4.10 同步 vs 异步：互不兼容

```python
def sync_func():
    return 42

async def main():
    sync_func()                  # OK，不阻塞
    await sync_func()            # TypeError（不是协程）
    await asyncio.sleep(0)       # OK
    time.sleep(1)                # 阻塞整个 event loop！别用
    asyncio.run(sync_func())     # 错（已经在 loop 里了）
```

**铁律**：

- `async def` 里调同步阻塞 IO = 阻塞整个 loop
- 同步代码里调 `await` = 错
- 同步与异步**不要混用**

## 4.11 同步库怎么接入 asyncio

用 `asyncio.to_thread`（3.9+）：

```python
import asyncio
import time

def blocking_io() -> int:
    time.sleep(1)
    return 42

async def main():
    result = await asyncio.to_thread(blocking_io)     # 不阻塞 loop
```

`asyncio.to_thread` 把同步函数扔到默认 executor（线程池），主协程继续跑。

## 4.12 错误：忘记 await

```python
async def main():
    coro = fetch("url")       # 没 await
    print(coro)               # 打印 coroutine object
    # 协程从未执行！Python 会给 "coroutine was never awaited" warning
```

**lint 工具（ruff）会标 `RUF006`**。开了 asyncio 规则后忘记 await 会立刻被发现。

## 4.13 入门清单

| API | 用途 |
|---|---|
| `asyncio.run` | 入口 |
| `asyncio.gather` | 并发 |
| `asyncio.create_task` | 调度 |
| `asyncio.sleep` | 异步等待 |
| `asyncio.to_thread` | 同步桥 |
| `async with` / `async for` | 异步协议 |
