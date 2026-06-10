# 阶段 1 项目：CLI TODO 工具

一个命令行 TODO 工具，把阶段 1 学到的所有概念串起来：

- 模块与包结构
- dataclass（用 dict 也行，阶段 4 会升级）
- JSON 持久化
- `argparse` 命令行解析
- 异常处理
- 单元测试 + 集成测试

## 功能

```bash
uv run python -m todo_cli add "Buy milk"
uv run python -m todo_cli list
uv run python -m todo_cli done 1
uv run python -m todo_cli remove 1
uv run python -m todo_cli clear
```

## 文件结构

```
project/
├── README.md           # 本文件
├── todo_cli/
│   ├── __init__.py
│   ├── __main__.py     # CLI 入口（argparse）
│   ├── models.py       # Todo 数据类
│   ├── storage.py      # JSON 持久化
│   ├── service.py      # 业务逻辑（add/list/done/remove/clear）
│   └── cli.py          # 命令行解析
└── tests/
    ├── __init__.py
    ├── test_service.py
    └── test_storage.py
```

## 任务清单

按顺序完成：

- [ ] 读 `models.py`，理解 `Todo` 的字段（dict 表示也行，阶段 4 会换成 `dataclass`）
- [ ] 实现 `storage.py` 的 `load_todos` / `save_todos`
- [ ] 实现 `service.py` 的五个操作
- [ ] 跑 `uv run pytest tests/` 全绿
- [ ] 实现 `cli.py` / `__main__.py`，让 CLI 可用
- [ ] 手动试一遍：add → list → done → list → remove → clear
- [ ] （可选）支持 `--file` 指定存储文件，便于测试

## 跑测试

```bash
cd stages/stage-01-basics
uv run pytest project/tests/ -v
```

## 设计要点

- `service` 不直接做文件 I/O，通过 `storage` 抽象（这样测试可以传临时目录）
- `Todo` 用 `id` 标识，`id` 在 add 时生成（用 `max(existing) + 1`，或 `uuid4`）
- list 时未完成排在前面
- 删除 / 完成 不存在的 id 要抛 `TodoNotFoundError`
