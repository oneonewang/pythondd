# 03 - `multiprocessing` 实战

## 3.1 为什么需要多进程

GIL 限制下，CPU 密集任务用线程**不会加速**。多进程 = 多份 Python 解释器 = 真正并行。

**代价**：

- 每个进程有独立内存（数十 MB）
- 进程间通信（IPC）比线程共享状态慢
- 启动开销比线程大

## 3.2 基本用法

```python
import multiprocessing as mp

def worker(x: int) -> int:
    return x * x

if __name__ == "__main__":
    with mp.Pool(processes=4) as pool:
        results = pool.map(worker, range(10))
    print(results)
```

> **重要**：多进程代码必须放在 `if __name__ == "__main__":` 下，否则 Windows / macOS 会无限递归 fork。

## 3.3 `ProcessPoolExecutor`：首选

```python
from concurrent.futures import ProcessPoolExecutor

def fib(n: int) -> int:
    return n if n < 2 else fib(n-1) + fib(n-2)

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(fib, [30, 31, 32, 33, 34, 35]))
    print(results)
```

接口与 `ThreadPoolExecutor` 一致——切换零成本。

## 3.4 进程间通信：`Queue` / `Pipe`

```python
import multiprocessing as mp

def producer(q: mp.Queue) -> None:
    for i in range(10):
        q.put(i)
    q.put(None)            # 哨兵

def consumer(q: mp.Queue) -> None:
    while True:
        item = q.get()
        if item is None:
            break
        print(item)

if __name__ == "__main__":
    q = mp.Queue()
    p1 = mp.Process(target=producer, args=(q,))
    p2 = mp.Process(target=consumer, args=(q,))
    p1.start(); p2.start()
    p1.join(); p2.join()
```

## 3.5 共享状态：`Value` / `Array` / `Manager`

```python
import multiprocessing as mp

def inc(counter):
    with counter.get_lock():
        counter.value += 1

if __name__ == "__main__":
    counter = mp.Value("i", 0)
    with mp.Pool(4) as pool:
        pool.map(inc, [counter] * 100)
    print(counter.value)        # 100
```

`Manager()` 可以共享任意 Python 对象（`list` / `dict`），但慢。

## 3.6 共享内存（Python 3.8+）

```python
import multiprocessing.shared_memory as shm

# 进程 A
shm_a = shm.SharedMemory(create=True, size=1024)
shm_a.buf[:4] = b"data"

# 进程 B（用 name 拿同一块）
shm_b = shm.SharedMemory(name=shm_a.name)
data = bytes(shm_b.buf[:4])     # b"data"
shm_b.close(); shm_a.unlink()
```

适合"传递大块数据"（如 numpy 数组、DataFrame）。

## 3.7 性能对比

```python
import time
from concurrent.futures import ProcessPoolExecutor

def cpu_heavy(n: int) -> int:
    s = 0
    for i in range(n):
        s += i * i
    return s

# 单进程
start = time.perf_counter()
[cpu_heavy(10_000_000) for _ in range(4)]
print(f"serial: {time.perf_counter() - start:.2f}s")   # 4.0s

# 4 进程
start = time.perf_counter()
with ProcessPoolExecutor(max_workers=4) as ex:
    list(ex.map(cpu_heavy, [10_000_000] * 4))
print(f"parallel: {time.perf_counter() - start:.2f}s") # 1.0s
```

## 3.8 适用场景

- 图像处理（OpenCV、Pillow）
- 数值计算（numpy / scipy）—— 已经多线程，multiprocessing 是叠加
- 压缩 / 解压
- 文本处理（大量正则、解析）
- ETL 中 CPU 密集阶段

**不适用**：

- 任务太小（启动开销 > 计算时间）
- 任务间需要频繁通信
- 需要共享大量状态

## 3.9 进程 vs 线程 vs 协程 速查

| 场景 | 用 |
|---|---|
| 单个 CPU 任务 | 直接跑 |
| 4-8 个 CPU 任务（独立） | `ProcessPoolExecutor(max_workers=CPU数)` |
| 100 个独立 IO 任务 | `ThreadPoolExecutor` 或 `asyncio` |
| 1000+ 高并发 IO | `asyncio` |
| 大数据计算 | numpy / polars / dask（已经多线程/多进程） |

## 3.10 调试坑

- **fork 后子进程可能继承父进程的 socket / 文件**——导致资源竞争
- **多进程 pickling 错误**：lambda / 闭包 / 文件句柄 / 数据库连接不能直接传
- **`if __name__ == "__main__"` 必备**：否则 main 模块会被 import 时也执行
- **macOS 默认 `spawn` 模式**：启动更慢
