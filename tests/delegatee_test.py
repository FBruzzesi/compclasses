from contextlib import nullcontext as does_not_raise
from typing import Sequence, Tuple

import pytest

from compclasses import delegatee


@pytest.mark.parametrize(
    "attr_name, expected",
    [
        ("__len__", True),
        ("__test__", True),
        ("__test", False),
        ("test__", False),
        ("test", False),
        ("_test_", False),
    ],
)
def test_is_dunder_method(attr_name: str, expected: bool):
    """Test for delegatee `_is_dunder_method` method"""

    assert delegatee._is_dunder_method(attr_name=attr_name) == expected


@pytest.mark.parametrize(
    "attrs, expected",
    [
        (("*",), ("a", "get_foo", "hello_from_foo")),
        (("__len__",), ("__len__",)),
        (("__len__", "*"), ("__len__", "a", "get_foo", "hello_from_foo")),
        (("__len__", "get_foo"), ("__len__", "get_foo")),
    ],
)
def test_parse_attrs(foo_cls, attrs: Sequence[str], expected: Tuple[str, ...]):
    """Test for delegatee `_parse_attrs` method"""
    delegatee_cls = foo_cls  # Foo

    assert set(delegatee._parse_attrs(delegatee_cls, attrs)) == set(expected)


@pytest.mark.parametrize(
    "attrs, expected",
    [
        (("__len__",), does_not_raise()),
        (("__len__", "a", "get_foo", "hello_from_foo"), does_not_raise()),
        (("*",), pytest.raises(AttributeError)),
        (("__add__",), pytest.raises(AttributeError)),
        (("some_fake_method",), pytest.raises(AttributeError)),
    ],
)
def test_validate_delegatee_methods(foo_cls, attrs: Sequence[str], expected):
    """Test for delegatee `_validate_delegatee_methods` method"""
    delegatee_cls = foo_cls  # Foo

    with expected:
        assert delegatee._validate_delegatee_methods(delegatee_cls, attrs) is None
