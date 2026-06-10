"""命令行入口。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import service, storage
from .service import TodoNotFoundError
from .storage import StorageError

DEFAULT_FILE = Path.home() / ".todo_cli.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="一个简单的 TODO 工具")
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_FILE,
        help=f"TODO 数据文件路径（默认 {DEFAULT_FILE}）",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="添加任务")
    p_add.add_argument("title", help="任务标题")

    sub.add_parser("list", help="列出任务")

    p_done = sub.add_parser("done", help="标记任务完成")
    p_done.add_argument("id", type=int)

    p_remove = sub.add_parser("remove", help="删除任务")
    p_remove.add_argument("id", type=int)

    sub.add_parser("clear", help="清空已完成")

    return parser


def render(todos: list[dict]) -> str:
    """把任务列表格式化成可读字符串。"""
    if not todos:
        return "（无任务）"
    lines = []
    for t in todos:
        marker = "x" if t["done"] else " "
        lines.append(f"[{marker}] {t['id']:>3}  {t['title']}  ({t['created_at']})")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        todos = storage.load_todos(args.file)
    except StorageError as e:
        print(f"读取失败：{e}", file=sys.stderr)
        return 1

    try:
        if args.command == "add":
            todo = service.add(todos, args.title)
            storage.save_todos(args.file, todos)
            print(f"已添加 #{todo['id']}：{todo['title']}")

        elif args.command == "list":
            print(render(service.list_todos(todos)))

        elif args.command == "done":
            todo = service.complete(todos, args.id)
            storage.save_todos(args.file, todos)
            print(f"已完成 #{todo['id']}：{todo['title']}")

        elif args.command == "remove":
            todo = service.remove(todos, args.id)
            storage.save_todos(args.file, todos)
            print(f"已删除 #{todo['id']}：{todo['title']}")

        elif args.command == "clear":
            n = service.clear_done(todos)
            storage.save_todos(args.file, todos)
            print(f"已清除 {n} 条已完成任务")

    except TodoNotFoundError as e:
        print(f"错误：{e}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
