"""内置规则集合：import 时自动注册到默认注册表。"""
from __future__ import annotations

from ..registry import get_default_registry
from .range_check import RangeCheck
from .required import RequiredField
from .type_check import TypeCheck

_registry = get_default_registry()
_registry.register_class(RequiredField)
_registry.register_class(TypeCheck)
_registry.register_class(RangeCheck)

__all__ = ["RangeCheck", "RequiredField", "TypeCheck"]
