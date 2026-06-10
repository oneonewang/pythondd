# Python 学习仓库

系统性学习 Python 的笔记、练习、项目。完整路线图见 [LEARNING_PLAN.md](./LEARNING_PLAN.md)。

## 目录

- [LEARNING_PLAN.md](./LEARNING_PLAN.md) — 完整学习路线图（8+ 阶段）
- `stages/stage-XX-...` — 每个阶段的讲解、练习、项目

## 当前进度

- ✅ **阶段 1** — 入门与工具链（已发布）
- ⏳ 阶段 2+ — 待启动

## 快速开始

```bash
# 安装 uv（如果还没有）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 进入任一阶段目录
cd stages/stage-01-basics
uv sync
uv run pytest          # 跑练习测试
uv run python project/  # 跑阶段项目
```

## 阶段一览

| 阶段 | 主题 | 状态 |
|---|---|---|
| 01 | 入门与工具链 | ✅ |
| 02 | Pythonic 核心 | ⏳ |
| 03 | 面向对象深入 | ⏳ |
| 04 | 类型系统与函数式 | ⏳ |
| 05 | 异步与并发 | ⏳ |
| 06 | 工程化 | ⏳ |
| 07 | 标准库精要 | ⏳ |
| 08+ | 方向选修 | ⏳ |
