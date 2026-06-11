# 01 - GIL 与并发模型选型

## 1.1 GIL 是什么

**GIL（Global Interpreter Lock）**：CPython 解释器的一把全局锁，**任何时刻只有一个线程能执行 Python 字节码**。

```python
# 看起来"并行"的两个线程
import threading

def cpu_heavy():
    s = 0
    for i in range(10_000_000):
        s += i
    return s

t1 = threading.Thread(target=cpu_heavy)
t2 = threading.Thread(target=cpu_heavy)
t1.start(); t2.start()
t1.join(); t2.join()
# 单核跑 ≈ 0.5s
# 双线程 ≈ 0.5s   （因为 GIL）—— 不会更快
```

> **GIL 的存在**让 CPython 的多线程**不能利用多核**做 CPU 密集工作。

**为什么要有 GIL**：

- 简化 CPython 内存管理（引用计数不用加锁）
- 大量 C 扩展（如 numpy）可以不加锁地访问 Python 对象
- 移除 GIL 的工作已经做了很多年（PEP 703），但还在实验

**Python 3.13+ 引入 free-threaded mode**（`--disable-gil` 编译选项），到 3.14/3.15 才会默认开启。现阶段：**写代码时仍要按"有 GIL"来设计**。

## 1.2 GIL 不影响什么

GIL 只阻止**同时**执行 Python 字节码。**IO 操作时会释放 GIL**：

- 文件读写
- 网络收发
- 数据库查询
- `time.sleep`
- 调 C 扩展（numpy / pandas 内部计算）

所以** IO 密集**任务用 threading 是有意义的（IO 等待时让其他线程跑）。

## 1.3 CPU 密集 vs IO 密集

### IO 密集（爬虫、DB 查询、文件 IO）

- **特点**：大部分时间在等 IO，单个任务"很闲"
- **解法**：
  - 简单并发：`threading` / `ThreadPoolExecutor`（IO 自动释放 GIL）
  - 高并发：**`asyncio`**（单线程、最少开销）

### CPU 密集（图像处理、数值计算、压缩）

- **特点**：纯 CPU 跑满了
- **解法**：
  - **`multiprocessing` / `ProcessPoolExecutor`**（多进程绕过 GIL）
  - 用 C 扩展（numpy / numba / Cython）
  - 换语言 / 用 PyPy / 等 free-threaded Python

### 混合

- 用 `ProcessPoolExecutor` 处理 CPU 部分，用 `asyncio` 处理 IO 部分
- 例如：先 `asyncio.gather` 拉一堆数据，再扔进 `ProcessPoolExecutor` 处理

## 1.4 三种并发模型对比

| 维度 | `threading` | `multiprocessing` | `asyncio` |
|---|---|---|---|
| 并行单元 | 线程 | 进程 | 协程 |
| 利用多核 | ❌（GIL） | ✅ | ❌ |
| 适合 | IO 密集 | CPU 密集 | 高并发 IO |
| 并发数 | 几十 ~ 几百 | 进程数 = CPU 核数 | **成千上万** |
| 内存开销 | 中（8MB/线程） | 高（数十 MB/进程） | 极低（KB/协程） |
| 编程模型 | 回调 / 锁 | 进程间通信 | `await` 链 |
| 调试难度 | 难（竞态） | 中（IPC） | 中（任务调度） |

## 1.5 选型决策树

```
你的任务是？
  ├─ CPU 密集
  │   ├─ 简单 → multiprocessing.Pool
  │   ├─ 函数式 + Python → ProcessPoolExecutor
  │   └─ 大量数据 → numpy / numba / polars / Cython
  └─ IO 密集
      ├─ 并发 < 100
      │   └─ ThreadPoolExecutor（最简单）
      ├─ 并发 100~10000
      │   └─ asyncio + aiohttp/httpx
      └─ 并发 > 10000
          └─ asyncio + 高性能生态（uvloop / asyncpg / redis.asyncio）
```

## 1.6 真实案例

| 场景 | 选 |
|---|---|
| 下载 100 张图 | `ThreadPoolExecutor(max_workers=20)` |
| 抓 10000 个 URL | `asyncio` + `httpx` + `Semaphore(50)` |
| 算 1 亿个数的和 | `ProcessPoolExecutor` + numpy |
| 跑 1000 个 SQL 查询 | `asyncio` + `asyncpg` |
| 读 100 个大文件解析 | `ThreadPoolExecutor` |
| Web 服务器（Flask / Django） | WSGI 线程 / ASGI 异步 |
| Web 服务器（FastAPI） | 全部 `asyncio` |

## 1.7 性能数字

- **threading vs serial IO**：N 个并发，理论快 N 倍（实际 5–10 倍）
- **multiprocessing vs serial CPU**：N 核，理论快 N 倍（实际 0.7–0.9N，IPC 开销）
- **asyncio vs serial IO**：N 个并发，理论快 N 倍（实际 50–200 倍，因为不用切换线程）
- **asyncio vs threading**：asyncio 内存和上下文切换都更省

## 1.8 概念辨析

| | 并发（concurrency） | 并行（parallelism） |
|---|---|---|
| 定义 | 多个任务**交替**推进 | 多个任务**真正同时**跑 |
| 例子 | 单核 CPU 跑两个进程（轮转） | 多核 CPU 跑两个进程 |
| asyncio | ✅ 高度并发 | ❌（单线程） |
| multiprocessing | ✅ 并发 | ✅ 真正并行 |

GIL 限制了 Python 的**并行**，但**并发**模型依然能利用 IO 等待时间。
