# 阶段 5 — 异步与并发

> 目标：理解 GIL 的真相、写出正确的并发代码。

## 计划内容

- GIL 真相、为什么 Python 多线程不一定快
- CPU 密集 → `multiprocessing` / `ProcessPoolExecutor`
- IO 密集 → `threading` / `ThreadPoolExecutor` / `asyncio`
- `asyncio` 基础：`coroutine` / `Task` / `await` / `event loop`
- `asyncio.gather` / `asyncio.wait` / 超时与取消
- 异步上下文管理器 / 异步生成器
- 异步生态：`aiohttp` / `httpx`

## 项目

异步并发爬虫：限速、重试、断点续爬、结果落库。

## 启动条件

阶段 4 项目通过。
