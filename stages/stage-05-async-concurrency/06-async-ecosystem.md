# 06 - 异步生态

## 6.1 HTTP：`httpx`（推荐）

`httpx` 同时支持同步和异步，API 与 `requests` 几乎一样。

```python
import httpx

# 同步
r = httpx.get("https://api.github.com", timeout=10)
print(r.status_code, r.json())

# 异步
async with httpx.AsyncClient(timeout=10) as client:
    r = await client.get("https://api.github.com")
    print(r.json())
```

**优势**：
- 同时支持 sync / async
- HTTP/2 支持（需要 `h2` 库）
- 流式响应
- 类型注解完善

## 6.2 `aiohttp`：纯异步老牌

```python
import aiohttp

async with aiohttp.ClientSession() as session:
    async with session.get(url) as r:
        data = await r.json()
```

API 风格和 httpx 略不同。httpx 是更现代的选择，**新项目用 httpx**。

## 6.3 异步文件 IO：`aiofiles`

```python
import aiofiles

async def read_file(path: str) -> str:
    async with aiofiles.open(path) as f:
        return await f.read()

async def write_file(path: str, content: str) -> None:
    async with aiofiles.open(path, "w") as f:
        await f.write(content)
```

**注意**：对**单个**大文件，aiofiles 不一定更快（OS 缓存 + 大块读取）。优势在**并发多个文件**。

## 6.4 数据库

### `asyncpg`（PostgreSQL）

```python
import asyncpg

async def main():
    conn = await asyncpg.connect("postgresql://...")
    rows = await conn.fetch("SELECT * FROM users WHERE age > $1", 18)
    await conn.close()
```

PostgreSQL 的最快 Python 驱动。

### `aiomysql`（MySQL）

```python
import aiomysql

async def main():
    pool = await aiomysql.create_pool(host="...", user="...", db="...")
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM users")
            rows = await cur.fetchall()
```

### `aiosqlite`（SQLite）

```python
import aiosqlite

async with aiosqlite.connect("db.sqlite") as db:
    await db.execute("CREATE TABLE IF NOT EXISTS t (x INTEGER)")
    await db.execute("INSERT INTO t VALUES (1)")
    async with db.execute("SELECT * FROM t") as cur:
        rows = await cur.fetchall()
```

**注意**：SQLite 单写者，async 收益有限。

## 6.5 Redis：`redis.asyncio`

```python
import redis.asyncio as redis

async def main():
    r = redis.Redis(host="localhost")
    await r.set("key", "value")
    val = await r.get("key")
    await r.aclose()
```

## 6.6 异步任务队列：`arq` / `taskiq` / `celery`

| 库 | 特点 |
|---|---|
| `arq` | 轻量，asyncio 原生，Redis 后端 |
| `taskiq` | 现代 asyncio 任务队列 |
| `celery` | 老牌、功能全、worker 进程模型 |

阶段 6 / 阶段 8 后端方向会再讲。

## 6.7 FastAPI：异步 Web 框架

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int) -> dict:
    return {"item_id": item_id}
```

FastAPI 是**纯异步**的 Web 框架，强烈推荐。

## 6.8 性能优化：`uvloop`

```python
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
```

`uvloop` 用 C 实现事件循环，**通常快 2–4 倍**。生产环境必装。

## 6.9 实战：异步 HTTP 客户端

```python
import asyncio
import time
import httpx

URLS = [f"https://httpbin.org/delay/0.1" for _ in range(50)]

async def fetch_all() -> None:
    async with httpx.AsyncClient(timeout=10) as client:
        async def one(url: str) -> int:
            r = await client.get(url)
            return r.status_code

        start = time.perf_counter()
        results = await asyncio.gather(*[one(u) for u in URLS])
        print(f"{len(results)} requests in {time.perf_counter() - start:.1f}s")
        # ~0.5s (并发 50 个 0.1s 延迟)

asyncio.run(fetch_all())
```

## 6.10 `asyncio` 速查

| 库 | 后端 / 用途 |
|---|---|
| `httpx` | HTTP 客户端（async + sync） |
| `aiohttp` | HTTP 客户端/服务端（纯 async） |
| `aiofiles` | 异步文件 IO |
| `asyncpg` | PostgreSQL 驱动 |
| `aiomysql` | MySQL 驱动 |
| `aiosqlite` | SQLite 驱动 |
| `redis.asyncio` | Redis 客户端 |
| `websockets` | WebSocket |
| `aiokafka` | Kafka 客户端 |
| `arq` / `taskiq` | 异步任务队列 |
| `uvloop` | C 实现事件循环 |
| `FastAPI` / `aiohttp.web` | 异步 Web 框架 |

## 6.11 同步库改异步

1. 用 `asyncio.to_thread(sync_func)`——简单
2. 找替代库（`requests` → `httpx`）
3. 大改：sockets 层用 `asyncio.open_connection`
