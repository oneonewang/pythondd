# 05 - 文件 I/O、模块、异常

## 5.1 文件 I/O

**永远用 `with`**（自动关闭）：

```python
# 读
with open("data.txt", encoding="utf-8") as f:
    text = f.read()           # 整个文件
    f.seek(0)
    lines = f.readlines()     # list[str]
    f.seek(0)
    for line in f:            # 逐行（推荐）
        print(line.rstrip())

# 写
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("hello\n")
    f.writelines(["a\n", "b\n"])

# 追加
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("another line\n")
```

**JSON**（最常用）：

```python
import json

# 读
with open("data.json", encoding="utf-8") as f:
    data = json.load(f)

# 写
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

**CSV**：

```python
import csv
with open("data.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])
```

## 5.2 路径：pathlib（不要再用 os.path）

```python
from pathlib import Path

p = Path("data") / "sub" / "file.txt"   # 跨平台拼路径
p.exists()
p.is_file()
p.is_dir()
p.parent
p.name         # "file.txt"
p.stem         # "file"
p.suffix       # ".txt"

# 读写
p.read_text(encoding="utf-8")
p.write_text("hello", encoding="utf-8")
p.read_bytes()

# 遍历
for f in Path("src").rglob("*.py"):   # 递归
    print(f)

# 创建
Path("out").mkdir(parents=True, exist_ok=True)
```

> 经验：阶段 1 可以用 `open()`，阶段 7 起统一用 `pathlib`。

## 5.3 模块与包

```python
# mypackage/utils.py
def greet(name):
    return f"hi {name}"

# mypackage/__init__.py   （可以是空文件，或暴露包级别 API）
from .utils import greet
```

```python
# 使用
from mypackage import greet
from mypackage.utils import greet
import mypackage.utils as u
```

**约定**：

- 包目录必须有 `__init__.py`（或者用 namespace package，3.3+）
- 模块名全小写、下划线分隔：`my_module`
- 类名 PascalCase：`MyClass`
- 函数 / 变量 snake_case：`my_func`
- 常量全大写：`MAX_SIZE`
- 私有用下划线开头：`_helper`

## 5.4 `if __name__ == "__main__"`

让文件既可作为脚本运行，也可被导入：

```python
# cli.py
def main():
    print("running as script")

if __name__ == "__main__":
    main()
```

直接跑 `python cli.py` 会执行 main；`import cli` 不会。

## 5.5 异常

**`try / except / else / finally`**：

```python
try:
    data = parse_input(text)
except ValueError as e:
    print(f"bad input: {e}")
else:
    process(data)         # 没异常才执行
finally:
    cleanup()             # 一定执行
```

**常见异常**：

- `ValueError` — 值不合法（`int("abc")`）
- `TypeError` — 类型错
- `KeyError` — dict 取不到
- `IndexError` — list 越界
- `FileNotFoundError` — 文件不存在
- `AttributeError` — 属性不存在

**`raise`**：

```python
def set_age(age):
    if age < 0:
        raise ValueError(f"age must be >= 0, got {age}")
```

**自定义异常**：

```python
class AppError(Exception):
    """所有应用错误的基类"""

class ConfigError(AppError):
    pass

raise ConfigError("missing API key")
```

> 经验：捕获具体异常，不要 `except Exception: pass`。

## 5.6 上下文管理器（阶段 2 详讲）

`with` 后面不只接文件，任意实现 `__enter__` / `__exit__` 的对象都可以：

```python
with open("f.txt") as f: ...
with lock: ...                    # threading.Lock
with conn.begin(): ...            # SQLAlchemy session
```

## 5.7 import 风格

```python
# 标准库
import os
import sys
from pathlib import Path

# 第三方
import requests
from fastapi import FastAPI

# 自己的
from myproject.utils import helper

# 不要这样
from os.path import *      # 命名空间污染
```

PEP 8 建议顺序：标准库 → 第三方 → 本地，组间空行分隔。`ruff` 自动帮你排。

## 5.8 常用标准库（阶段 7 详讲）

- `os` / `sys` / `pathlib` — 文件、系统
- `json` / `csv` / `tomllib` — 数据
- `collections` — `Counter` / `defaultdict` / `deque`
- `itertools` / `functools` — 函数式
- `typing` — 类型
- `logging` — 日志
- `argparse` / `click` — CLI
- `unittest` / `pytest` — 测试
