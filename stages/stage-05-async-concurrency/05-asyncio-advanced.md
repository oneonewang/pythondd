# 05 - `asyncio` 进阶

## 5.1 任务取消

```python
import asyncio

async def long_task():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("cancelled!")
        raise     # 必须 re-raise

async def main():
    t = asyncio.create_task(long_task())
    await asyncio.sleep(1)
    t.cancel()                 # 触发 CancelledError
    try:
        await t
    except asyncio.CancelledError:
        print("task cancelled")
```

**被取消的协程拿到 `CancelledError`**。必须正确清理（关闭文件、关闭连接），然后**reraise**（不 re-raise 会出现幽灵 bug）。

## 5.2 超时：`asyncio.wait_for`

```python
import asyncio

async def fetch(url: str) -> str:
    await asyncio.sleep(2)
    return "data"

async def main():
    try:
        result = await asyncio.wait_for(fetch("..."), timeout=1.0)
    except asyncio.TimeoutError:
        print("timeout!")
```

`wait_for` 内部 = 创建 task + 定时 cancel。

## 5.3 `asyncio.shield`：保护不被取消

```python
async def main():
    try:
        result = await asyncio.wait_for(asyncio.shield(critical_task()), timeout=1)
    except asyncio.TimeoutError:
        # critical_task 还在跑，await 它收尾
        result = await critical_task()
```

`shield` 阻止外部 cancel 传到内部协程。**保护"不能中断"的关键操作**（如关闭连接、提交事务）。

## 5.4 `gather` 异常处理

```python
# 默认：任何一个异常，gather 抛
results = await asyncio.gather(c1, c2, c3)            # 失败抛

# return_exceptions=True：异常当结果
results = await asyncio.gather(c1, c2, c3, return_exceptions=True)
# results: [result1, ValueError(...), result3]
```

**实战**：

```python
results = await asyncio.gather(*tasks, return_exceptions=True)
for url, r in zip(urls, results):
    if isinstance(r, Exception):
        log_failure(url, r)
    else:
        process(r)
```

## 5.5 `gather` vs `wait`

| | `gather` | `wait` |
|---|---|---|
| 返回 | 全部结果（按输入顺序） | `done` / `pending` 两个集合 |
| 取消行为 | 一个失败全部取消 | 灵活 |
| 超时 | 不支持 | 支持 `timeout=` |
| 适用 | "等所有完成" | "先处理完成的" |

```python
done, pending = await asyncio.wait(
    [asyncio.create_task(c) for c in coros],
    timeout=1.0,
    return_when=asyncio.FIRST_COMPLETED,
)
```

`return_when`：
- `FIRST_COMPLETED`：第一个完成就返回
- `FIRST_EXCEPTION`：第一个异常 OR 全部完成
- `ALL_COMPLETED`（默认）：全部完成

## 5.6 `as_completed`：实时处理

```python
for coro in asyncio.as_completed(coros):
    result = await coro
    process(result)             # 谁先完成谁先处理
```

## 5.7 `Semaphore`：限速

```python
sem = asyncio.Semaphore(10)            # 最多 10 个并发

async def fetch(url: str) -> str:
    async with sem:
        return await real_fetch(url)

# 1000 个 URL，最多 10 个同时发
results = await asyncio.gather(*[fetch(u) for u in urls])
```

`Semaphore(n)` = 同一时刻最多 n 个协程进入"临界区"。

## 5.8 `Lock`：互斥

```python
lock = asyncio.Lock()

async def critical():
    async with lock:
        await do_io()                 # 其他协程等到 lock 释放
```

**注意**：asyncio 的 `Lock` 是**协作式**的，协程必须主动 `await` 才会让出。同步代码里的 `Lock` 是抢占式。

## 5.9 `Event`：跨协程通知

```python
event = asyncio.Event()

async def waiter():
    await event.wait()                # 等到 set
    print("event!")

async def setter():
    await asyncio.sleep(1)
    event.set()                       # 唤醒所有 waiter

await asyncio.gather(waiter(), setter())
```

## 5.10 `Queue`：异步队列

```python
queue: asyncio.Queue[int] = asyncio.Queue()

async def producer():
    for i in range(10):
        await queue.put(i)

async def consumer():
    while True:
        item = await queue.get()
        if item is None:
            break
        process(item)
        queue.task_done()
```

## 5.11 异常与回调

```python
def on_done(task: asyncio.Task) -> None:
    try:
        result = task.result()
    except Exception as e:
        log(e)
    else:
        process(result)

task = asyncio.create_task(some_coro())
task.add_done_callback(on_done)
```

## 5.12 后台任务

```python
async def main():
    task = asyncio.create_task(heartbeat())
    try:
        await do_main_work()
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
```

## 5.13 调试

```python
# 看当前所有 task
import asyncio
asyncio.all_tasks()

# 启调试模式（3.7+）
asyncio.run(main(), debug=True)

# 慢回调警告（100ms+）
import warnings
warnings.simplefilter("always", ResourceWarning)
```

## 5.14 反模式

```python
# 1. 在 async def 里调 time.sleep
async def bad():
    time.sleep(1)                # 阻塞 loop

# 2. 在 async def 里用 requests
import requests
async def bad():
    requests.get(...)            # 同步 IO，阻塞

# 3. 把 await 忘了
async def bad():
    fetch(url)                   # coroutine never awaited

# 4. asyncio.run 嵌套
async def bad():
    asyncio.run(other_coro())    # RuntimeError
```

## 5.15 综合实战：限速爬虫

```python
import asyncio
import httpx

sem = asyncio.Semaphore(10)
client = httpx.AsyncClient(timeout=10)

async def fetch(url: str) -> dict:
    async with sem:
        for attempt in range(3):
            try:
                r = await client.get(url)
                r.raise_for_status()
                return r.json()
            except Exception as e:
                if attempt == 2:
                    raise
                await asyncio.sleep(2 ** attempt)

async def crawl(urls: list[str]) -> list[dict]:
    tasks = [fetch(u) for u in urls]
    return await asyncio.gather(*tasks, return_exceptions=True)
```
