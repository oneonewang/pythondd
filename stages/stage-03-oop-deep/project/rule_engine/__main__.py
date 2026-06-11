"""CLI 入口。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import loader
from .engine import RuleEngine
from .registry import get_default_registry


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="rule-engine", description="可扩展规则引擎")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="列出已注册规则")

    p_eval = sub.add_parser("evaluate", help="对输入跑规则")
    p_eval.add_argument("--input", "-i", required=True, help="JSON 字符串 或 @file.json")
    p_eval.add_argument(
        "--plugins",
        nargs="*",
        default=[],
        help="额外加载的插件模块路径列表",
    )

    p_explain = sub.add_parser("explain", help="解释某条规则")
    p_explain.add_argument("rule", help="规则名")

    return p


def _read_input(spec: str) -> dict:
    if spec.startswith("@"):
        return json.loads(Path(spec[1:]).read_text(encoding="utf-8"))
    return json.loads(spec)


def cmd_list(args: argparse.Namespace) -> int:
    registry = get_default_registry()
    engine = RuleEngine(registry)
    for name in engine.list_rules():
        rule = registry.get(name)
        print(f"{name:<20} priority={rule.priority}")
    return 0


def cmd_evaluate(args: argparse.Namespace) -> int:
    if args.plugins:
        loader.load_from_modules(args.plugins, get_default_registry())

    data = _read_input(args.input)
    engine = RuleEngine(get_default_registry())
    report = engine.evaluate(data)

    for result in report.results:
        marker = "✓" if result.passed else "✗"
        print(f"  {marker} {result.rule_name:<20} {result.message}")
    print()
    print(f"==> {report.summary()}")

    return 0 if report.passed else 1


def cmd_explain(args: argparse.Namespace) -> int:
    engine = RuleEngine(get_default_registry())
    try:
        print(engine.explain(args.rule))
    except KeyError:
        print(f"未找到规则：{args.rule}", file=sys.stderr)
        return 1
    return 0


_COMMANDS = {
    "list": cmd_list,
    "evaluate": cmd_evaluate,
    "explain": cmd_explain,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return _COMMANDS[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
