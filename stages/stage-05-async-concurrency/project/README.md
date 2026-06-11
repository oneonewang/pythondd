# 阶段 5 项目：异步并发爬虫

**目标**：写一个工业级异步爬虫：限速 + 重试 + 超时 + 持久化 + 断点续爬。

## 功能

```bash
# 跑爬虫：限速 10 并发、超时 10s、最多重试 3 次
uv run python -m async_crawler crawl --urls sample_data/urls.txt --db results.db

# 断点续爬：处理上次失败/未完成的 URL
uv run python -m async_crawler resume --db results.db

# 查看统计
uv run python -m async_crawler stats --db results.db
```

## 文件结构

```
project/
├── README.md
├── async_crawler/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── models.py
│   ├── protocols.py
│   ├── rate_limiter.py
│   ├── retry.py
│   ├── storage.py
│   ├── fetcher.py
│   └── crawler.py
└── tests/
    ├── __init__.py
    ├── test_crawler.py
    ├── test_retry.py
    ├── test_rate_limiter.py
    └── test_storage.py
```

## 设计

- **`Fetcher` Protocol**：`async def fetch(url) -> FetchResult`——可注入 `HttpxFetcher` / `MockFetcher`
- **`RateLimiter`**：基于 `asyncio.Semaphore` 的限速器
- **`retry` 装饰器**：指数退避（1s → 2s → 4s）
- **`SQLiteStorage`**：用 `sqlite3` 持久化（同步、跨进程；或 `aiosqlite`）
- **`Crawler`**：编排 fetch + retry + limit + save

## 任务清单

- [ ] `models.py`：`FetchResult`（url / status / content / error）
- [ ] `protocols.py`：`Fetcher` Protocol
- [ ] `rate_limiter.py`：基于 `asyncio.Semaphore` 的 `RateLimiter`
- [ ] `retry.py`：指数退避装饰器
- [ ] `storage.py`：SQLite 持久化（建表 / upsert / 查询失败）
- [ ] `fetcher.py`：`HttpxFetcher` + `MockFetcher`
- [ ] `crawler.py`：`AsyncCrawler` 主类
- [ ] CLI：`crawl` / `resume` / `stats`
- [ ] 跑 `uv run pytest` 全绿
- [ ] 跑 `uv run mypy` 通过

## 核心约束

- 所有 HTTP 调用必须用 `httpx.AsyncClient`
- 用 `asyncio.Semaphore(max_concurrent)` 限速
- 用 `asyncio.wait_for` 实现单请求超时
- 失败用指数退避（最多 3 次）
- 全程不阻塞 event loop
