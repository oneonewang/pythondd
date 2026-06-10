# 01 - 环境与工具链

## 1.1 为什么用 uv 而不是 venv + pip

`venv + pip` 工作流：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi
pip freeze > requirements.txt
```

问题：

- `pip install` 不解析依赖冲突，遇到大项目会很痛
- `requirements.txt` 不锁子依赖（要 `pip freeze` 才能锁）
- 多 Python 版本管理要靠 `pyenv` / 系统包管理器

`uv`（[astral.sh/uv](https://docs.astral.sh/uv/)，用 Rust 写的）一次解决：

- 解析依赖（与 pip 兼容的索引，但有锁文件 `uv.lock`）
- 安装比 pip 快 10–100 倍
- 自带 Python 版本管理（不用 pyenv）
- 兼容 `pyproject.toml`

## 1.2 安装 uv 与 Python

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 Python 3.12（首次会自动下载）
uv python install 3.12
```

## 1.3 初始化项目

```bash
cd stages/stage-01-basics
uv init .          # 在当前目录初始化（生成 pyproject.toml）
uv python pin 3.12 # 把 Python 版本写进 .python-version
uv add pytest ruff mypy
```

`pyproject.toml` 是项目的"配置中心"，所有现代 Python 工具（构建、测试、lint、类型）都从这里读。

## 1.4 日常命令

```bash
uv run python xxx.py   # 临时跑脚本
uv run pytest          # 跑测试
uv add requests        # 加运行时依赖
uv add --dev pytest    # 加开发依赖
uv sync                # 按 lock 文件同步环境
uv lock                # 重新生成 lock 文件
```

## 1.5 REPL

REPL = Read-Eval-Print Loop，交互式解释器，是你写 Python 的核心工具。

```bash
$ uv run python
>>> 1 + 2
3
>>> import this    # 经典彩蛋
```

**强烈推荐装 IPython**（或更新的 `python -i` 已够用）：

```bash
uv add --dev ipython
uv run ipython
```

IPython 提供的便利：

- `?obj` / `obj?` 看帮助
- `obj.<TAB>` 自动补全
- `_` `_` 引用上上次结果
- `%timeit` `%paste` 等魔法命令

## 1.6 调试小技巧

```bash
# 跑完脚本后进入 REPL，保留现场
uv run python -i xxx.py

# 看一个对象的全部属性
uv run python -c "import requests; print(dir(requests))"

# 找某个函数的定义
uv run python -c "import inspect, requests; print(inspect.getsourcefile(requests.get))"
```

## 1.7 编辑器

推荐 VSCode + Python 扩展（自带 Pylance，类型检查一流）。其他选择：PyCharm、Neovim + pyright。

## 1.8 必装开发工具

```bash
uv add --dev pytest ruff mypy
```

- **pytest**：测试运行器
- **ruff**：lint + format（一个顶 flake8 + isort + black）
- **mypy**：静态类型检查（阶段 3 起常用）

## 小结

- 用 `uv` 统一管环境、依赖、Python 版本
- 用 `pyproject.toml` 表达项目元信息
- 写代码前先用 REPL 验证假设
- 编辑器装 Pylance，写代码就有类型提示
