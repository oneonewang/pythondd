"""生成测试用的样本日志（小）。"""
from datetime import datetime, timedelta


def make_sample(path, n_lines: int = 1000, error_rate: float = 0.05) -> None:
    """生成 ``n_lines`` 行日志，错误率约 ``error_rate``。"""
    base = datetime(2024, 1, 15, 10, 0, 0)
    levels = ["INFO", "INFO", "INFO", "INFO", "INFO", "WARN", "INFO", "ERROR"]
    with path.open("w", encoding="utf-8") as f:
        for i in range(n_lines):
            ts = (base + timedelta(seconds=i)).isoformat(timespec="seconds")
            level = levels[i % len(levels)]
            f.write(f"{ts} {level} sample message line {i}\n")


if __name__ == "__main__":
    import sys
    from pathlib import Path

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("sample_data/app.log")
    out.parent.mkdir(parents=True, exist_ok=True)
    make_sample(out, n)
    print(f"wrote {n} lines to {out}")
