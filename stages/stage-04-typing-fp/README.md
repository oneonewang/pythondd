# 阶段 4 — 类型系统与函数式

> 目标：用类型系统给代码加"自动文档"，用函数式习惯写出更简洁的逻辑。

## 计划内容

- `typing` 基础：`list[int]`（3.9+） / `Optional` / `Union` / `TypeAlias` / `NewType` / `TypeVar`
- `Generic[T]` 与泛型类
- `Protocol` 与结构化子类型
- `dataclass` / `frozen=True` / `__post_init__`
- `functools`：`lru_cache` / `partial` / `reduce` / `singledispatch`
- `itertools`：`chain` / `islice` / `groupby` / `tee` / `permutations`
- 模式匹配 `match ... case`

## 项目

类型安全的数据管线：`dataclass` 流转 + `mypy --strict` 校验。

## 启动条件

阶段 3 项目通过。
