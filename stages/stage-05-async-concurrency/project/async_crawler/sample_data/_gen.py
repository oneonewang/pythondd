"""生成测试用 URL 列表。"""
from pathlib import Path


def make_urls(path: Path, n: int = 20) -> None:
    """生成 n 个示例 URL。"""
    urls = [
        f"https://httpbin.org/get?n={i}"
        for i in range(n)
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(urls), encoding="utf-8")


if __name__ == "__main__":
    import sys

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    out = (
        Path(sys.argv[2])
        if len(sys.argv) > 2
        else Path(__file__).parent / "sample_data" / "urls.txt"
    )
    make_urls(out, n)
    print(f"wrote {n} URLs to {out}")
