# 阶段 3 项目：可扩展规则引擎

一个**用 Protocol 抽象 + 插件化注册**的规则引擎。

## 概念

- **规则（Rule）**：检查输入数据是否满足某条件（类型、范围、必填等）
- **引擎（Engine）**：把规则按优先级排序、对输入依次执行、聚合结果
- **注册表（Registry）**：管理"已注册的规则类"，支持插件化加载
- **插件（Plugin）**：任何实现了 `Rule` 协议的 Python 类

## 协议

```python
class Rule(Protocol):
    name: str
    priority: int

    def evaluate(self, data: dict) -> RuleResult: ...
    def explain(self) -> str: ...
```

不强制继承——只要"形状对"就行。

## CLI

```bash
uv run python -m rule_engine list
uv run python -m rule_engine evaluate --input '{"name": "alice", "age": 30}'
uv run python -m rule_engine explain required_field
uv run python -m rule_engine evaluate --input '{...}' --plugins my_project.custom_rules
```

## 文件结构

```
project/
├── README.md
├── rule_engine/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── protocols.py
│   ├── registry.py
│   ├── engine.py
│   ├── loader.py
│   ├── models.py
│   └── builtin_rules/
│       ├── __init__.py
│       ├── required.py
│       ├── type_check.py
│       └── range_check.py
└── tests/
    ├── __init__.py
    ├── test_engine.py
    ├── test_registry.py
    └── test_builtin.py
```

## 任务清单

- [ ] `models.py`：`RuleResult`（pass/fail + message）
- [ ] `protocols.py`：`Rule` 协议
- [ ] `registry.py`：`RuleRegistry`，管理类到实例的映射
- [ ] `engine.py`：`RuleEngine` 执行规则、聚合结果
- [ ] `loader.py`：`load_from_module("mod.path")` 动态 import
- [ ] 内置 3 个规则：required / type_check / range_check
- [ ] CLI：`list` / `evaluate` / `explain`
- [ ] 跑 `uv run pytest` 全绿
- [ ] 写一个"外部插件"类证明 Protocol 模式可用

## 核心约束

- 用 `Protocol` + 鸭子类型，不强制继承
- 注册表全局单例（`get_default_registry()`）
- 规则按 `priority` 降序执行（高优先级先跑）
- 引擎在 `evaluate` 失败时仍跑完所有规则，收集所有错误
