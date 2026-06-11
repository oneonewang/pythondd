"""插件加载：按字符串路径动态 import，触发模块里的注册逻辑。"""
from __future__ import annotations

import importlib
from collections.abc import Iterable
from typing import Any

from .registry import RuleRegistry


def load_from_module(module_path: str, registry: RuleRegistry | None = None) -> int:
    """import 一个模块，返回该模块新注册了几个规则。

    模块级约定：模块 import 时会调用 ``registry.register_class(...)``。
    """
    # TODO
    raise NotImplementedError


def load_from_modules(
    module_paths: Iterable[str],
    registry: RuleRegistry | None = None,
) -> int:
    """批量 import。返回总注册数。"""
    # TODO
    raise NotImplementedError
