# 阶段 4 项目：类型安全数据管线

多阶段数据转换管线，全程 dataclass + Protocol + Generic。

## 数据流

```
RawRecord (dict)
    └─→ ParsedRecord
            └─→ ValidatedRecord
                    └─→ EnrichedRecord
                            └─→ Summary
```

## 设计

- **每阶段是 dataclass(frozen=True)**：不可变、可哈希
- **每阶段用 Protocol 抽象**：`Transformer[T, U]`、`Validator[T]`、`Enricher[T, U]`
- **Pipeline 是 Generic 容器**：`Pipeline[T, U]` 接受 `Transformer[T, U]`
- **格式化用 singledispatch**：`format_value(int|float|str|list|dict)` 按类型分派
- **mypy --strict 通过**

## CLI

```bash
uv run python -m data_pipeline run --input @sample_data/users.json
uv run python -m data_pipeline validate --input @sample_data/users.json
uv run python -m data_pipeline summary --input @sample_data/users.json
```

## 文件结构

```
project/
├── README.md
├── data_pipeline/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── models.py
│   ├── protocols.py
│   ├── pipeline.py
│   ├── formatters.py
│   ├── errors.py
│   └── stages/
│       ├── __init__.py
│       ├── parser.py
│       ├── validator.py
│       ├── enricher.py
│       └── aggregator.py
└── tests/
    ├── __init__.py
    ├── test_parser.py
    ├── test_validator.py
    ├── test_enricher.py
    ├── test_aggregator.py
    └── test_pipeline.py
```

## 任务清单

- [ ] `models.py`：所有 dataclass
- [ ] `protocols.py`：Transformer / Validator / Enricher Protocol
- [ ] `errors.py`：ValidationError
- [ ] `pipeline.py`：Pipeline 通用容器
- [ ] `formatters.py`：singledispatch 格式化
- [ ] `stages/parser.py`：dict → ParsedRecord
- [ ] `stages/validator.py`：ParsedRecord → ValidatedRecord | error
- [ ] `stages/enricher.py`：ValidatedRecord → EnrichedRecord
- [ ] `stages/aggregator.py`：Iterable[EnrichedRecord] → Summary
- [ ] CLI：`run` / `validate` / `summary`
- [ ] 跑 `uv run pytest` 全绿
- [ ] 跑 `uv run mypy data_pipeline --strict` 全清

## 核心约束

- 所有 `models` 都是 `frozen=True`
- `Transformer` 是 `Protocol[T, U]`
- `Validator` 返回 `T | None`（None 表示失败）
- `Pipeline` 用 `Generic[T, U]` 表达阶段类型
- `mypy --strict` 零错误
