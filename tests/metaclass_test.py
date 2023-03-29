from contextlib import nullcontext as does_not_raise
from typing import Callable, Tuple, Type

import pytest

from compclasses import CompclassMeta, delegatee

def has_all_attrs(cls: Type, attrs: Tuple[str], prefix: str, suffix: str):
    """Checks that cls has all attributes in attrs"""
    for attr in attrs:

        attr_name = (
            attr if delegatee._is_dunder_method(attr) else f"{prefix}{attr}{suffix}"
        )
        assert hasattr(cls, attr_name)

# TODO
