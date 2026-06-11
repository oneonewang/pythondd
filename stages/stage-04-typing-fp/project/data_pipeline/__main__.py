"""CLI 入口。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .errors import ValidationError
from .models import EnrichedRecord, ParsedRecord, ValidatedRecord
from .stages.aggregator import SummaryAggregator
from .stages.enricher import RecordEnricher
from .stages.parser import DictParser
from .stages.validator import RecordValidator


def _read_json(spec: str) -> list[dict[str, object]]:
    if spec.startswith("@"):
        return json.loads(Path(spec[1:]).read_text(encoding="utf-8"))
    return json.loads(spec)


def _run_pipeline(raw: list[dict]) -> tuple[list[EnrichedRecord], list[ValidationError]]:
    """跑完整管线，返回 (成功, 失败)。"""
    parser_ = DictParser()
    validator = RecordValidator()
    enricher = RecordEnricher()

    valid_records: list[ValidatedRecord] = []
    errors: list[ValidationError] = []
    parsed: list[ParsedRecord] = []

    # parse
    for i, r in enumerate(raw):
        try:
            parsed.append(parser_.parse(r))
        except (ValueError, KeyError, TypeError) as e:
            errors.append(ValidationError(f"row{i}", str(e)))

    # validate
    for p in parsed:
        v = validator.validate(p)
        if v is None:
            errors.append(ValidationError(p.record_id, "validation failed"))
        else:
            valid_records.append(v)

    # enrich
    enriched = [enricher.enrich(v) for v in valid_records]
    return enriched, errors


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="data-pipeline", description="类型安全数据管线")
    sub = p.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="完整跑管线，输出 Summary JSON")
    p_run.add_argument("--input", "-i", required=True)
    p_run.add_argument("--output", "-o", help="可选，输出 Summary JSON 到文件")

    sub.add_parser("validate", help="只跑 parse + validate")
    sub.add_parser("summary", help="跑完整管线 + Summary")
    return p


def cmd_run(args: argparse.Namespace) -> int:
    raw = _read_json(args.input)
    enriched, errors = _run_pipeline(raw)
    summary = SummaryAggregator().aggregate(enriched)

    print(f"raw={len(raw)} ok={len(enriched)} errors={len(errors)}")
    for e in errors:
        print(f"  {e}")
    print()
    print("Summary:")
    print(f"  total: {summary.total}")
    print(f"  total_usd: {summary.total_usd:.2f}")
    print(f"  by_action: {summary.by_action}")
    print(f"  by_category: {summary.by_category}")

    if args.output:
        Path(args.output).write_text(
            json.dumps(
                {
                    "total": summary.total,
                    "total_usd": summary.total_usd,
                    "by_action": summary.by_action,
                    "by_category": summary.by_category,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    raw = _read_json(args.input)
    enriched, errors = _run_pipeline(raw)
    print(f"valid={len(enriched)} errors={len(errors)}")
    for e in errors:
        print(f"  {e}")
    return 0 if not errors else 1


def cmd_summary(args: argparse.Namespace) -> int:
    return cmd_run(args)


_COMMANDS = {"run": cmd_run, "validate": cmd_validate, "summary": cmd_summary}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return _COMMANDS[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
