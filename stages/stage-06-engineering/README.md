# 阶段 6 — 工程化

> 目标：把练习代码变成可发布、可维护、可观测的工程产物。

## 计划内容

- `pyproject.toml` 完整解读（PEP 621）
- 打包：`hatchling` / `uv build` / `setuptools`
- 测试：`pytest`、fixture、parametrize、monkeypatch、mock
- 覆盖率：`coverage.py`
- Lint/Format：`ruff`
- 静态类型：`mypy --strict` / `pyright`
- 日志：`logging` 最佳实践
- 性能：`cProfile` / `py-spy` / `line_profiler`
- CI：GitHub Actions 跑测试 + lint + 类型检查

## 项目

把阶段 5 的爬虫打包成可发布的 CLI 工具。

## 启动条件

阶段 5 项目通过。
