"""CLI 入口。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import analyzer, parser


def build_parser() -> argparse.ArgumentParser:
    parser_ = argparse.ArgumentParser(
        prog="log-analyzer",
        description="流式日志分析器（生成器管道，O(1) 内存）",
    )
    parser_.add_argument("logfile", type=Path, help="日志文件路径")
    sub = parser_.add_subparsers(dest="command", required=True)

    sub.add_parser("summary", help="各 level 计数")

    p_errors = sub.add_parser("errors", help="前 N 条 ERROR")
    p_errors.add_argument("--limit", type=int, default=10)

    p_rate = sub.add_parser("rate", help="滑动窗口错误率")
    p_rate.add_argument("--window", type=int, default=100)
    p_rate.add_argument("--level", default="ERROR")
    p_rate.add_argument("--limit", type=int, default=20, help="最多输出多少行")

    p_anom = sub.add_parser("anomalies", help="错误率超阈值的窗口")
    p_anom.add_argument("--window", type=int, default=100)
    p_anom.add_argument("--threshold", type=float, default=0.1)
    p_anom.add_argument("--level", default="ERROR")

    return parser_


def cmd_summary(args: argparse.Namespace) -> int:
    stats = parser.ParseStats()
    counts = analyzer.count_by_level(analyzer.analyze_file(args.logfile, stats=stats))
    print(f"total={stats.total_lines} parsed={stats.parsed} errors={stats.errors}")
    for level, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {level:<8} {n}")
    return 0


def cmd_errors(args: argparse.Namespace) -> int:
    rec_iter = analyzer.analyze_file(args.logfile)
    for r in analyzer.take_errors(rec_iter, args.limit):
        print(f"{r.timestamp} {r.level} {r.message}")
    return 0


def cmd_rate(args: argparse.Namespace) -> int:
    rec_iter = analyzer.analyze_file(args.logfile)
    for anomaly in analyzer.sliding_rate(rec_iter, args.window, args.level):
        print(
            f"line {anomaly.line_no:>6}  "
            f"{anomaly.level} rate = {anomaly.error_rate:.2%}  "
            f"(window={anomaly.window_size})"
        )
    return 0


def cmd_anomalies(args: argparse.Namespace) -> int:
    rec_iter = analyzer.analyze_file(args.logfile)
    flagged = analyzer.find_anomalies(
        rec_iter, args.window, args.threshold, args.level
    )
    for anomaly in flagged:
        print(
            f"[ALERT] line {anomaly.line_no}: "
            f"{anomaly.error_rate:.2%} > {args.threshold:.2%}"
        )
    return 0


_COMMANDS = {
    "summary": cmd_summary,
    "errors": cmd_errors,
    "rate": cmd_rate,
    "anomalies": cmd_anomalies,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.logfile.exists():
        print(f"文件不存在：{args.logfile}", file=sys.stderr)
        return 1
    return _COMMANDS[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
