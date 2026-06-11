# 阶段 5 — 异步与并发

> 目标：理解 GIL 的真相、写出正确的并发代码。

## 学习目标

完成后你将能：

- 解释为什么 Python 多线程不一定快（GIL）
- 选择正确的并发模型（threading / multiprocessing / asyncio）
- 用 `asyncio` 写高并发 IO 代码
- 协调多个协程：gather / wait / 超时 / 取消
- 用 `aiohttp` / `httpx` 异步 HTTP
- 用 `asyncio.Semaphore` 限速
- 给爬虫加：限速 + 重试 + 超时 + 持久化

## 知识点（按顺序读）

1. [01-gil-and-concurrency.md](./01-gil-and-concurrency.md) — GIL 真相、CPU 密集 vs IO 密集、选型
2. [02-threading.md](./02-threading.md) — `threading` 实战、`Lock` / `ThreadPoolExecutor`
3. [03-multiprocessing.md](./03-multiprocessing.md) — `multiprocessing` / `ProcessPoolExecutor`
4. [04-asyncio-basics.md](./04-asyncio-basics.md) — coroutine / Task / await / event loop
5. [05-asyncio-advanced.md](./05-asyncio-advanced.md) — gather / wait / 超时 / 取消 / 异步上下文管理器
6. [06-async-ecosystem.md](./06-async-ecosystem.md) — `aiohttp` / `httpx` / 异步生态

## 练习

```bash
cd stages/stage-05-async-concurrency
uv sync
uv run pytest -v
```

| 编号 | 主题 | 关键练习点 |
|---|---|---|
| ex01 | GIL 与 threading | 用 `time.perf_counter` 验证 IO 密集能并行 |
| ex02 | multiprocessing | 用 `ProcessPoolExecutor` 并行 CPU 计算 |
| ex03 | asyncio 基础 | 写协程、Task、`asyncio.gather` |
| ex04 | asyncio 进阶 | 超时、取消、异步上下文管理器 |
| ex05 | 异步 IO | 用 `aiofiles` 模拟异步文件 IO |

## 项目：异步并发爬虫

进入 `project/`，按 `README.md` 指引实现。

需求：

- 给一组 URL 并发 fetch（默认 200 个，限速 10 并发）
- 每个 fetch 有超时（默认 10s）
- 失败重试（指数退避，最多 3 次）
- 结果存到 SQLite，支持断点续爬
- 持久化失败的 URL 以便重试
- CLI：`crawl` / `resume` / `stats`

## 阶段完成标志

- `uv run pytest` 全绿
- 爬虫能处理 1000+ URL 且内存 < 100 MB
- 你能口述：GIL 是啥、为什么 asyncio 单线程能并发、`gather` vs `wait` 的差异
