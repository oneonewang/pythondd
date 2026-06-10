# 阶段 2 项目：流式日志分析器

一个**不把日志全部读进内存**的日志分析器，全程用生成器管道。

## 功能

```bash
uv run python -m log_analyzer summary path/to/app.log
uv run python -m log_analyzer errors path/to/app.log --limit 20
uv run python -m log_analyzer rate path/to/app.log --window 100 --level ERROR
uv run python -m log_analyzer anomalies path/to/app.log --window 100 --threshold 0.1
```

## 日志格式

默认支持：

```
2024-01-15T10:23:45 INFO User logged in user_id=123
2024-01-15T10:23:46 ERROR Database connection failed timeout=30s
2024-01-15T10:23:47 WARN  Slow query duration=1.2s
```

字段：`<ISO 时间> <LEVEL> <message>`

## 文件结构

```
project/
├── README.md
├── sample_data/
│   └── app.log            # 测试用的小日志
├── log_analyzer/
│   ├── __init__.py
│   ├── __main__.py        # CLI 入口
│   ├── cli.py             # argparse
│   ├── parser.py          # 解析器（生成器）
│   ├── analyzer.py        # 流式统计
│   └── models.py          # LogRecord 数据类
└── tests/
    ├── __init__.py
    ├── test_parser.py
    └── test_analyzer.py
```

## 任务清单

- [ ] 实现 `parser.py`：`iter_records(path)` 生成器，按行解析
- [ ] 实现 `analyzer.py`：
  - `count_by_level(records)` 计数器
  - `take_errors(records, n)` 取最近 n 条 ERROR
  - `sliding_rate(records, window, level)` 滑动窗口错误率
  - `find_anomalies(records, window, threshold)` 错误率超阈值报警
- [ ] 实现 `cli.py` / `__main__.py`：四个子命令
- [ ] 跑 `uv run pytest tests/` 全绿
- [ ] 生成 1 GB 测试日志（用脚本），跑通后内存 < 100 MB

## 核心约束

- `parser` / `analyzer` 全部用生成器/迭代器，不出现 `list(...)` 把全文件读入
- 单个函数最长不超过 30 行
- 解析失败的行不抛异常，计入 `parser.errors` 计数

## 设计要点

**生成器管道**（参考阶段 2 讲解文档）：

```
file
  └─ iter_lines()          [生成器]
       └─ iter_records()   [生成器，附带错误计数]
            └─ count_by_level() / take_errors() / sliding_rate()
```

每一步都是惰性的、内存 O(1)。
