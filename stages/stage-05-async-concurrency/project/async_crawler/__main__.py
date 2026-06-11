"""CLI 入口。"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from .crawler import AsyncCrawler, CrawlerConfig
from .fetcher import HttpxFetcher
from .storage import SQLiteStorage


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="async-crawler", description="异步并发爬虫")
    sub = p.add_subparsers(dest="command", required=True)

    p_crawl = sub.add_parser("crawl", help="爬一批 URL")
    p_crawl.add_argument("--urls", required=True, help="URL 文件（每行一个）")
    p_crawl.add_argument("--db", required=True, help="SQLite 数据库路径")
    p_crawl.add_argument("--max-concurrent", type=int, default=10)
    p_crawl.add_argument("--timeout", type=float, default=10.0)
    p_crawl.add_argument("--max-retries", type=int, default=3)

    p_resume = sub.add_parser("resume", help="断点续爬：处理上次失败/未完成的")
    p_resume.add_argument("--db", required=True)
    p_resume.add_argument("--max-concurrent", type=int, default=10)
    p_resume.add_argument("--timeout", type=float, default=10.0)
    p_resume.add_argument("--max-retries", type=int, default=3)

    p_stats = sub.add_parser("stats", help="查看统计")
    p_stats.add_argument("--db", required=True)

    return p


def _read_urls(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


async def _run_crawl(args: argparse.Namespace) -> int:
    urls = _read_urls(Path(args.urls))
    storage = SQLiteStorage(Path(args.db))
    fetcher = HttpxFetcher(timeout=args.timeout)
    config = CrawlerConfig(
        max_concurrent=args.max_concurrent,
        timeout=args.timeout,
        max_retries=args.max_retries,
    )
    crawler = AsyncCrawler(fetcher, storage, config)

    print(f"crawling {len(urls)} URLs (max_concurrent={args.max_concurrent})...")
    results = await crawler.crawl(urls)

    ok = sum(1 for r in results if r.ok)
    failed = len(results) - ok
    print(f"done. ok={ok} failed={failed}")
    storage.close()
    return 0 if failed == 0 else 1


async def _run_resume(args: argparse.Namespace) -> int:
    storage = SQLiteStorage(Path(args.db))
    pending = storage.get_pending() + storage.get_failed()
    print(f"resuming {len(pending)} URLs...")
    fetcher = HttpxFetcher(timeout=args.timeout)
    config = CrawlerConfig(
        max_concurrent=args.max_concurrent,
        timeout=args.timeout,
        max_retries=args.max_retries,
    )
    crawler = AsyncCrawler(fetcher, storage, config)
    results = await crawler.crawl(pending)
    print(f"done. ok={sum(1 for r in results if r.ok)}")
    storage.close()
    return 0


def _run_stats(args: argparse.Namespace) -> int:
    storage = SQLiteStorage(Path(args.db))
    stats = storage.stats()
    print(json.dumps(stats, indent=2))
    storage.close()
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "crawl":
        return asyncio.run(_run_crawl(args))
    if args.command == "resume":
        return asyncio.run(_run_resume(args))
    if args.command == "stats":
        return _run_stats(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
