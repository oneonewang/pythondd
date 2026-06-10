# 阶段 2 — Pythonic 核心

> 目标：写出"地道"的 Python 代码。本阶段是 Python 区别于其他语言最显著的地方。

## 学习目标

完成后你将能：

- 用推导式替代累加器循环
- 用生成器把"流"作为一等公民
- 写装饰器横切关注点（日志、计时、缓存、重试）
- 用 `with` 包装任意资源的获取/释放
- 用魔术方法让自定义类型"用起来像内置类型"
- 不靠继承，靠协议（鸭子类型）解耦

## 知识点（按顺序读）

1. [01-comprehensions.md](./01-comprehensions.md) — list / dict / set 推导式、生成器表达式
2. [02-iterators-and-generators.md](./02-iterators-and-generators.md) — 迭代器协议、`yield`、`yield from`
3. [03-decorators.md](./03-decorators.md) — 函数装饰器、类装饰器、`functools.wraps`
4. [04-context-managers.md](./04-context-managers.md) — `with` 协议、`contextlib`
5. [05-magic-methods.md](./05-magic-methods.md) — 魔术方法（dunder）实战
6. [06-duck-typing.md](./06-duck-typing.md) — 协议、鸭子类型、EAFP

## 练习

```bash
cd stages/stage-02-pythonic-core
uv sync
uv run pytest -v
```

| 编号 | 主题 | 关键练习点 |
|---|---|---|
| ex01 | 推导式 | list/dict/set、嵌套、可读 vs 性能权衡 |
| ex02 | 迭代器与生成器 | 自定义 `__iter__`/`__next__`、`yield`、`yield from` |
| ex03 | 装饰器 | 计时、日志、参数校验、装饰链 |
| ex04 | 上下文管理器 | `__enter__`/`__exit__`、`contextlib.contextmanager` |
| ex05 | 魔术方法 | 让自定义集合支持 `len`/`in`/`for`/`==` |

## 项目：流式日志分析器

进入 `project/`，按 `README.md` 指引实现。

需求：

- 解析大日志文件（GB 级），全程用生成器，不一次性读入内存
- 子命令：
  - `summary` — 各 level（INFO/WARN/ERROR）计数
  - `errors` — 输出最近 N 条 ERROR
  - `rate` — 滑动窗口错误率
  - `anomalies` — 错误率超阈值时报警
- 核心管线 = 纯函数生成器，可单独测试

## 阶段完成标志

- `uv run pytest` 全绿
- 项目能解析 1 GB 测试日志且内存占用 < 100 MB
- 你能口述：迭代器协议、生成器、装饰器、上下文管理器分别解决什么问题
