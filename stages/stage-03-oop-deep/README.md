# 阶段 3 — 面向对象深入

> 目标：掌握 Python 独有的 OOP 特性——描述符、MRO、Protocol/ABC、`__slots__`、多继承。

## 学习目标

完成后你将能：

- 理解 `super()` 和 MRO 的真实工作原理
- 自己实现一个描述符（`__get__` / `__set__` / `__delete__`）
- 解释 `property` / `staticmethod` / `classmethod` 在字节码层是什么
- 在 `ABC` 和 `Protocol` 之间做对的选择
- 用 `__slots__` 优化内存
- 用 Mixin 组合横切能力

## 知识点（按顺序读）

1. [01-class-basics-and-mro.md](./01-class-basics-and-mro.md) — `__init__` / `__new__`、继承、`super()`、MRO C3 线性化
2. [02-descriptors.md](./02-descriptors.md) — 描述符协议、`property`、方法、`staticmethod` / `classmethod` 真相
3. [03-attribute-protocol.md](./03-attribute-protocol.md) — `__getattr__` / `__setattr__` / `__getattribute__` / `__delattr__`
4. [04-abc-vs-protocol.md](./04-abc-vs-protocol.md) — 抽象基类 vs 结构化子类型、何时用哪个
5. [05-slots-and-memory.md](./05-slots-and-memory.md) — `__slots__`、内存布局、什么时候值得用
6. [06-multiple-inheritance.md](./06-multiple-inheritance.md) — 多继承、Mixin、菱形问题、组合

## 练习

```bash
cd stages/stage-03-oop-deep
uv sync
uv run pytest -v
```

| 编号 | 主题 | 关键练习点 |
|---|---|---|
| ex01 | 类与 MRO | `__init__` / `__new__`、`super()`、菱形 MRO |
| ex02 | 描述符 | 自己写 `__get__`/`__set__`、实现 typed property |
| ex03 | 属性协议 | `__getattr__` 代理模式、`__setattr__` 验证 |
| ex04 | ABC 与 Protocol | 写 ABC、写 Protocol、用 `runtime_checkable` |
| ex05 | slots 与 Mixin | 用 `__slots__` 优化、用 Mixin 组合能力 |

## 项目：可扩展规则引擎

进入 `project/`，按 `README.md` 指引实现。

需求：

- 用 `Protocol` 定义 `Rule` 接口（`name` / `priority` / `evaluate` / `explain`）
- `RuleRegistry` 管理规则的注册、查询、按优先级排序
- `RuleEngine` 接收输入（dict）、执行所有规则、聚合结果
- CLI：
  - `evaluate` — 对输入跑所有规则，输出结果
  - `list` — 列出已注册规则
  - `explain <rule>` — 解释某条规则的逻辑
- 支持**插件加载**：从 Python 模块路径动态导入规则类

## 阶段完成标志

- `uv run pytest` 全绿
- 引擎能加载至少 3 个内置规则（类型检查 / 范围检查 / 必填字段）
- 能从外部模块加载新规则
- 你能口述：描述符、MRO、ABC vs Protocol 各自的本质区别
