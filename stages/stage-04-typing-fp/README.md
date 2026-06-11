# 阶段 4 — 类型系统与函数式

> 目标：用类型系统给代码加"自动文档"，用函数式习惯写出更简洁的逻辑。

## 学习目标

完成后你将能：

- 写出能通过 `mypy --strict` 的代码
- 用 `Generic[T]` 表达容器
- 用 `Protocol` + 结构化子类型解耦
- 用 `@dataclass` 替代手写 `__init__` / `__repr__` / `__eq__`
- 用 `functools` 工具（`lru_cache` / `partial` / `singledispatch`）简化代码
- 用 `itertools` 高效处理序列
- 用 `match ... case` 做结构化解构

## 知识点（按顺序读）

1. [01-typing-fundamentals.md](./01-typing-fundamentals.md) — 基础类型提示（`list[T]` / `Optional` / `Union` / `Annotated`）
2. [02-typevar-and-generics.md](./02-typevar-and-generics.md) — `TypeVar`、泛型类、`ParamSpec`
3. [03-protocol-advanced.md](./03-protocol-advanced.md) — Protocol 实战、`Self`、结构化子类型
4. [04-dataclass.md](./04-dataclass.md) — `@dataclass` 完整能力
5. [05-functools.md](./05-functools.md) — `lru_cache` / `partial` / `reduce` / `singledispatch` / `cached_property`
6. [06-itertools-and-match.md](./06-itertools-and-match.md) — `itertools` 必知 + 模式匹配

## 练习

```bash
cd stages/stage-04-typing-fp
uv sync
uv run pytest -v
```

| 编号 | 主题 | 关键练习点 |
|---|---|---|
| ex01 | typing 基础 | `list[T]` / `Optional` / `Union` / `TypedDict` / `Literal` / `NewType` |
| ex02 | 泛型 | `TypeVar`、自定义 `Stack[T]` / `Pair[K, V]` |
| ex03 | Protocol 进阶 | `Self` 返回类型、`runtime_checkable`、组合 Protocol |
| ex04 | dataclass | `frozen`、`slots`、`__post_init__`、`field(default_factory=...)` |
| ex05 | functools | `lru_cache`、`partial`、`singledispatch`、`cached_property` |

## 项目：类型安全数据管线

进入 `project/`，按 `README.md` 指引实现。

需求：

- 读 JSON / CSV 输入，每条记录经过 4 阶段：
  1. **parse** — `dict` → `RawRecord`
  2. **validate** — `RawRecord` → `ValidatedRecord`（或 `ValidationError`）
  3. **enrich** — `ValidatedRecord` → `EnrichedRecord`（加派生字段）
  4. **aggregate** — `Iterable[EnrichedRecord]` → `Summary`（统计）
- 每阶段用 `dataclass(frozen=True)` 表达
- 用 `Protocol` 定义转换器接口
- 用 `Generic[T, U]` 表达 `Transformer[T, U]`
- 用 `singledispatch` 按类型分发
- CLI：`run` / `validate` / `summary`

## 阶段完成标志

- `uv run pytest` 全绿
- 项目 `mypy --strict` 通过
- 你能口述：`TypeVar` 和 `Generic` 解决什么问题、`Protocol` 与 `ABC` 的本质差异、`functools` 5 个常用工具各自的用途
