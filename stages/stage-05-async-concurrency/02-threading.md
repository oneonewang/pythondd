# 02 - `threading` 实战

## 2.1 基本用法

```python
import threading

def worker(name: str) -> None:
    print(f"{name} start")
    # do something
    print(f"{name} done")

t1 = threading.Thread(target=worker, args=("t1",))
t2 = threading.Thread(target=worker, args=("t2",))
t1.start(); t2.start()
t1.join(); t2.join()
```

## 2.2 线程安全问题

```python
counter = 0

def inc():
    global counter
    for _ in range(100_000):
        counter += 1     # 不是原子的！

t1 = threading.Thread(target=inc)
t2 = threading.Thread(target=inc)
t1.start(); t2.start()
t1.join(); t2.join()
print(counter)            # 不一定是 200000，可能更少
```

`counter += 1` 实际是 `LOAD / ADD / STORE` 三步，多线程会相互覆盖。

## 2.3 `Lock`：互斥锁

```python
lock = threading.Lock()
counter = 0

def inc():
    global counter
    for _ in range(100_000):
        with lock:
            counter += 1
```

**经验**：能用消息队列就别共享状态；能"线程局部"就别加锁。

## 2.4 线程局部存储：`threading.local`

```python
import threading

storage = threading.local()

def set_user(name: str) -> None:
    storage.user = name

def get_user() -> str:
    return storage.user

# 每个线程看到自己的 storage.user
```

`requests.Session` 之类的库用它实现"每个线程一个连接"。

## 2.5 `ThreadPoolExecutor`：首选

直接用 `threading.Thread` 容易失控，**用 `concurrent.futures.ThreadPoolExecutor`** 更安全：

```python
from concurrent.futures import ThreadPoolExecutor
import time

def fetch(url: str) -> str:
    time.sleep(0.5)              # 模拟 IO
    return f"result for {url}"

urls = [f"http://example.com/{i}" for i in range(10)]

with ThreadPoolExecutor(max_workers=5) as ex:
    results = list(ex.map(fetch, urls))

# 10 个 fetch × 0.5s 单线程 = 5s
# 5 线程并发 ≈ 1s
```

## 2.6 `submit` vs `map`

```python
with ThreadPoolExecutor(max_workers=5) as ex:
    # submit：返回 Future
    futures = [ex.submit(fetch, url) for url in urls]
    results = [f.result() for f in futures]

    # map：惰性，按输入顺序返回（适合参数同质）
    results = list(ex.map(fetch, urls))
```

## 2.7 处理异常

```python
with ThreadPoolExecutor() as ex:
    futures = [ex.submit(risky, x) for x in xs]
    for f in futures:
        try:
            result = f.result()
        except Exception as e:
            print(f"task failed: {e}")
```

`Future.result()` 会重新抛出工作线程里的异常。

## 2.8 `as_completed`：谁先完成谁先返回

```python
from concurrent.futures import as_completed

with ThreadPoolExecutor() as ex:
    futures = {ex.submit(fetch, url): url for url in urls}
    for f in as_completed(futures):
        url = futures[f]
        try:
            print(url, f.result())
        except Exception as e:
            print(url, "failed:", e)
```

适合"谁快谁先处理"（比如实时显示进度）。

## 2.9 `daemon` 线程

```python
t = threading.Thread(target=background_worker, daemon=True)
t.start()
```

`daemon=True` 的线程主程序退出时会被强制结束。**用于后台心跳、日志写入等**。

## 2.10 实战：线程池下载

```python
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import httpx

def download(url: str, dest: Path) -> None:
    with httpx.stream("GET", url, timeout=10) as r:
        r.raise_for_status()
        dest.write_bytes(r.read())

with ThreadPoolExecutor(max_workers=8) as ex:
    futures = [ex.submit(download, u, p) for u, p in pairs]
    for f in futures:
        f.result()
```

## 2.11 GIL 下的实际加速

```python
# IO 密集：能加速
urls = [...]
start = time.perf_counter()
serial_fetch_all(urls)         # 10s
print(time.perf_counter() - start)

with ThreadPoolExecutor(max_workers=10) as ex:
    list(ex.map(serial_fetch_all, urls))   # 1-2s
print(time.perf_counter() - start)

# CPU 密集：基本不加速
def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)
with ThreadPoolExecutor(8) as ex:
    list(ex.map(fib, [35] * 8))   # 不会比单线程快
```

## 2.12 常见坑

1. **GIL 误判**：以为多线程一定快。CPU 密集它不快。
2. **死锁**：两个锁交叉等待——保持加锁顺序一致。
3. **异常吞掉**：线程内异常不显式处理会"消失"。**用 `Future.result()`**。
4. **资源泄漏**：线程池忘记 `with`——`executor.shutdown()` 不调，程序挂着。
5. **共享状态竞态**：能用队列就用队列，能用 `local` 就用 `local`，别共享变量。
