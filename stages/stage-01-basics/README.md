# 阶段 1 — 入门与工具链

> 目标：从其他语言背景平滑过渡到 Python 的基本工作流。会讲什么不同、什么一样、什么一定要改掉。

## 学习目标

完成后你将能：

- 用 `uv` 独立管理项目环境和依赖
- 熟练使用 REPL 做实验
- 写出符合 Python 风格的基础代码
- 完成一个可用的 CLI TODO 工具

## 知识点（按顺序读）

1. [01-env-and-tools.md](./01-env-and-tools.md) — Python 安装、uv、REPL、工具链
2. [02-syntax-basics.md](./02-syntax-basics.md) — 缩进、变量、类型、控制流
3. [03-data-structures.md](./03-data-structures.md) — list / tuple / set / dict
4. [04-functions.md](./04-functions.md) — 函数定义、参数、解包、作用域
5. [05-io-and-modules.md](./05-io-and-modules.md) — 文件 I/O、模块、`__main__`、异常

## 练习

进入 `exercises/` 目录，按编号顺序完成。每道题在对应 `exNN_*.py` 里写实现，测试在 `test_exNN_*.py`。

```bash
cd stages/stage-01-basics
uv sync
uv run pytest -v          # 跑所有练习
uv run pytest exercises/test_ex01_*.py -v   # 跑单个练习
```

| 编号 | 主题 | 关键练习点 |
|---|---|---|
| ex01 | 变量、类型、字符串 | 动态类型、字符串格式化、不可变性 |
| ex02 | 集合操作 | list/tuple/set/dict 选型、推导式雏形 |
| ex03 | 函数 | 默认参数、可变参数、解包 |
| ex04 | 文件与异常 | `with`、异常捕获、自定义异常 |
| ex05 | 惯用法 | 看到 non-pythonic 改写为 pythonic |

## 项目：CLI TODO 工具

进入 `project/`，按 `README.md` 指引实现一个命令行 TODO 工具。

功能：

- `add <title>` — 添加任务
- `list` — 列出所有任务（未完成优先）
- `done <id>` — 标记完成
- `remove <id>` — 删除任务
- `clear` — 清空已完成

要求：

- 用 JSON 文件持久化
- 核心逻辑（不依赖 CLI）必须有单元测试
- 写一个 `Makefile` 或 `task runner` 跑测试

## 阶段完成标志

- `uv run pytest` 全绿
- `project/README.md` 里所有命令都能跑通
- 你能口述 Python 与你之前语言的 5 个最大差异
