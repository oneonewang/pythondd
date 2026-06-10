# Python 系统学习计划

> 面向"有其他语言经验、Python 从 0"的工程师。每阶段交付：**讲解文档 + 练习代码 + 小项目**。

## 设计原则

1. **对比驱动**：不重复你已经会的概念，直接讲 Python 的差异点（动态类型、鸭子类型、协议、描述符、GIL）。
2. **惯用法优先**：从一开始就用 Pythonic 写法。`non_pythonic` vs `pythonic` 对照是核心。
3. **测试驱动练习**：练习用 pytest 验证，提交即可跑。
4. **真实项目**：每个阶段的小项目来自真实场景（CLI 工具、爬虫、API、ETL），不刷算法题。
5. **工具链统一**：uv（环境/包） + pytest（测试） + ruff（lint/format） + mypy（类型）。

## 阶段总览

| 阶段 | 主题 | 周期 | 核心收获 |
|---|---|---|---|
| 1 | 入门与工具链 | 5 天 | 环境、REPL、基础语法、数据结构、I/O |
| 2 | Pythonic 核心 | 7 天 | 推导式、生成器、装饰器、上下文管理器、魔术方法 |
| 3 | 面向对象深入 | 7 天 | 类/MRO、描述符、property、元类、Protocol/ABC |
| 4 | 类型系统与函数式 | 6 天 | typing、Generic、Protocol、functools、itertools、模式匹配 |
| 5 | 异步与并发 | 7 天 | GIL 真相、asyncio、threading、multiprocessing、实战爬虫 |
| 6 | 工程化 | 6 天 | pytest、pyproject.toml、打包、logging、profiling、CI |
| 7 | 标准库精要 | 6 天 | collections、pathlib、dataclasses、pydantic、subprocess、argparse |
| 8 | 方向选修 ×N | 4–6 周/方向 | 后端 / 数据 / ML / 自动化 / DevOps |

> 阶段 8 之后按方向分叉，可二选一或多个组合。

## 学习节奏

- **每天 1–2 小时**：1 个主题（文档 30 分钟）+ 2–3 道练习（30–60 分钟）+ 当天项目功能增量（30 分钟）。
- **周末 2–4 小时**：完成本周 mini-project，提交后进入下一阶段。
- **学习方式**：每个阶段我先把讲解文档和项目骨架建好，你跟着写练习、跑测试、补完项目功能。

## 目录结构

```
pythondd/
├── README.md                  # 入口说明
├── LEARNING_PLAN.md           # 本文件
├── stages/
│   ├── stage-01-basics/
│   │   ├── README.md          # 阶段说明
│   │   ├── 01-env-and-tools.md
│   │   ├── 02-syntax-basics.md
│   │   ├── 03-data-structures.md
│   │   ├── 04-functions.md
│   │   ├── 05-io-and-modules.md
│   │   ├── exercises/         # 带 pytest 验证的练习
│   │   │   ├── test_ex01_*.py
│   │   │   └── ...
│   │   └── project/           # 阶段项目
│   │       └── ...
│   ├── stage-02-pythonic-core/
│   ├── ...
```

## 阶段详细

### 阶段 1 — 入门与工具链
- Python 与其他语言的"第一印象"差异
- uv 安装、虚拟环境、依赖管理
- REPL / IPython / `python -i`
- 基本语法：缩进、注释、变量、动态类型
- 数据结构：`list` / `tuple` / `set` / `dict`
- 控制流：`if` / `for` / `while` / `match`（3.10+）
- 函数基础：参数、返回值、作用域
- 文件 I/O、模块、`__main__`
- **项目**：命令行 TODO 工具（增删改查 + JSON 持久化）

### 阶段 2 — Pythonic 核心
- 推导式：list/dict/set comprehension
- 迭代器协议：`__iter__` / `__next__`
- 生成器与 `yield` / `yield from`
- 装饰器：基础、带参、类装饰器、`functools.wraps`
- 上下文管理器：`with` / `__enter__` / `__exit__` / `contextlib`
- 魔术方法：`__repr__` / `__str__` / `__eq__` / `__hash__` / `__len__` / `__getitem__` / `__call__`
- 鸭子类型与"接口靠协议"
- **项目**：流式日志分析器（读取大文件 → 生成器管道 → 统计）

### 阶段 3 — 面向对象深入
- 类基础、`__init__` / `__new__`
- 继承、MRO（`C3` 线性化）、`super()`
- 多继承与菱形问题
- `property` 描述符协议
- `__getattr__` / `__setattr__` / `__getattribute__`
- 描述符（descriptor）深入：方法、property、`staticmethod` / `classmethod` 真相
- `__slots__` 与内存优化
- ABC（`abc.ABCMeta`） vs `typing.Protocol`（结构化子类型）
- **项目**：可扩展的规则引擎（用协议定义接口、注册插件）

### 阶段 4 — 类型系统与函数式
- `typing` 基础：`List` / `Dict` / `Optional` / `Union`（Python 3.9+ 可直接用 `list[int]`）
- `TypeAlias` / `NewType` / `TypeVar`
- `Generic[T]` 与泛型类
- `Protocol` 与结构化子类型
- `dataclass` / `frozen=True` / `__post_init__`
- `functools`：`lru_cache` / `partial` / `reduce` / `singledispatch`
- `itertools`：`chain` / `islice` / `groupby` / `tee` / `permutations`
- 模式匹配 `match ... case`
- **项目**：类型安全的数据管线（dataclass 流转 + mypy strict 校验）

### 阶段 5 — 异步与并发
- GIL 真相、为什么 Python 多线程不一定快
- CPU 密集 → `multiprocessing` / `ProcessPoolExecutor`
- IO 密集 → `threading` / `ThreadPoolExecutor` / `asyncio`
- `asyncio` 基础：`coroutine` / `Task` / `await` / `event loop`
- `asyncio.gather` / `asyncio.wait` / 超时与取消
- 异步上下文管理器 / 异步生成器
- 异步生态：`aiohttp` / `httpx`
- **项目**：异步并发爬虫（限速、重试、断点续爬、结果落库）

### 阶段 6 — 工程化
- `pyproject.toml` 完整解读（PEP 621）
- 打包：`hatchling` / `uv build` / `setuptools`
- 测试：`pytest`、fixture、parametrize、monkeypatch、mock
- 覆盖率：`coverage.py`
- Lint/Format：`ruff`（替代 flake8+isort+black）
- 静态类型：`mypy --strict` / `pyright`
- 日志：`logging` 最佳实践（不要 print）
- 性能：`cProfile` / `py-spy` / `line_profiler`
- CI：GitHub Actions 跑测试 + lint + 类型检查
- **项目**：把阶段 5 的爬虫打包成可发布的 CLI 工具

### 阶段 7 — 标准库精要
- `collections`：`Counter` / `defaultdict` / `OrderedDict` / `ChainMap` / `deque`
- `pathlib` 取代 `os.path`
- `dataclasses` vs `attrs` vs `pydantic`
- `subprocess` 安全调用外部命令
- `argparse` / `click` / `typer`
- `concurrent.futures` 统一线程/进程池
- `typing` 高级：`TypedDict` / `Literal` / `Final` / `Annotated`
- **项目**：带子命令的本地工具集（init / run / inspect / clean）

### 阶段 8+ — 方向选修（择 1–N）

**A. 后端 Web**
- HTTP 基础、REST 设计
- **FastAPI**：路由、依赖注入、Pydantic 模型、中间件、OAuth2、测试
- 数据库：SQLAlchemy 2.0（同步 + 异步）、Alembic 迁移
- 缓存与队列：Redis / Celery / arq
- 部署：Docker、Gunicorn/Uvicorn、Nginx
- **结业项目**：博客或短链服务

**B. 数据分析 / 数据工程**
- NumPy：ndarray、广播、向量化
- pandas：DataFrame、分组聚合、时间序列
- Polars：更快的大数据 DataFrame
- 可视化：matplotlib / plotly
- ETL：Arrow / Parquet / DuckDB
- **结业项目**：销售数据 ETL + 仪表盘

**C. AI / 机器学习**
- 数值基础：NumPy / SciPy
- 经典 ML：scikit-learn 流水线
- 深度学习：PyTorch 基础（张量、自动求导、训练循环）
- LLM 应用：HuggingFace、LangChain / LlamaIndex、prompt engineering
- **结业项目**：RAG 知识库问答

**D. 自动化 / DevOps**
- 脚本：glob、shutil、subprocess
- CLI 工具：click / typer
- 配置：YAML/TOML、pydantic-settings
- Ansible 替代：fabric / mitogen
- **结业项目**：服务器巡检 + 报表机器人

## 工具链约定

```bash
# 全程用 uv（也可换 poetry / pdm / hatch）
uv python install 3.12
uv init stage-XX
uv add pytest ruff mypy
uv run pytest
uv run ruff check .
uv run mypy .
```

## 完成标准

- **练习**：每个 stage 下的 `exercises/` 跑 `uv run pytest` 全绿。
- **项目**：能独立运行，含 `README.md` 说明功能与运行方式。
- **类型**：阶段 3 起逐步引入类型，阶段 6 后所有项目 `mypy --strict` 通过。
