"""生成测试用的样本数据。"""
import json
from pathlib import Path


def make_sample(path: Path, n: int = 20) -> None:
    records = []
    for i in range(n):
        records.append(
            {
                "record_id": f"r{i}",
                "user_id": i % 3 + 1,
                "timestamp": f"2024-01-{(i // 5) + 1:02d}T10:{i % 60:02d}:00",
                "action": ["buy", "sell", "deposit", "withdraw"][i % 4],
                "amount": 50.0 + i * 10,
                "currency": ["USD", "EUR", "JPY", "CNY", "GBP"][i % 5],
            }
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import sys

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    out = (
        Path(sys.argv[2])
        if len(sys.argv) > 2
        else Path(__file__).parent / "sample_data" / "users.json"
    )
    make_sample(out, n)
    print(f"wrote {n} records to {out}")
