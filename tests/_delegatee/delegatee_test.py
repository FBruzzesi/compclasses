from contextlib import nullcontext as does_not_raise
from typing import Iterable, Tuple
from unittest import mock

import pytest

from compclasses import delegatee


@pytest.mark.parametrize(
    "attrs",
    [None, list(), tuple()],
)
def test_empty_attrs(foo_cls, attrs: Iterable[str]):
    """Test for delegatee init with empty attrs param"""

    with pytest.raises(ValueError):
        delegatee(foo_cls, attrs=attrs)


@pytest.mark.parametrize(
    "null_cls, expected",
    [
        (False, 1),
        (True, 0),
    ],
)
def test_init_parse_attrs_call(foo_cls, null_cls: bool, expected: int):
    """Tests whether or not _parse_attrs method is called depending on delegatee_cls"""

    delegatee_cls = foo_cls if not null_cls else None
    attrs: Iterable[str] = ("get_foo", "hello_from_foo")

    with mock.patch.object(delegatee, "_parse_attrs") as parse_attrs_mock:
        _ = delegatee(delegatee_cls, attrs=attrs)
        assert parse_attrs_mock.call_count == expected


@pytest.mark.parametrize(
    "null_cls, validate, expected",
    [
        (False, True, 1),
        (False, False, 0),
        (True, False, 0),
        (True, False, 0),
    ],
)
def test_init_validate_call(foo_cls, null_cls: bool, validate: bool, expected: int):
    """
    Tests whether or not _validate_delegatee_methods method
    is called depending on delegatee_cls and validate param
    """
    delegatee_cls = foo_cls if not null_cls else None
    attrs: Iterable[str] = ("get_foo", "hello_from_foo")

    with mock.patch.object(delegatee, "_validate_delegatee_methods") as validate_mock:
        _ = delegatee(delegatee_cls, attrs=attrs, validate=validate)
        assert validate_mock.call_count == expected


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
        (("__len__",), ("__len__",)),
        (("__len__", "get_foo"), ("__len__", "get_foo")),
        (("__len__", "*"), ("__len__", "a", "_foo", "get_foo", "hello_from_foo")),
        (("*",), ("a", "_foo", "get_foo", "hello_from_foo")),
    ],
)
def test_parse_attrs(foo_cls, attrs: Iterable[str], expected: Tuple[str, ...]):
    """Test for delegatee `_parse_attrs` method"""
    delegatee_cls = foo_cls  # Foo

    assert set(delegatee._parse_attrs(delegatee_cls, attrs)) == set(expected)


@pytest.mark.parametrize(
    "attrs, context",
    [
        (("__len__",), does_not_raise()),
        (("__len__", "a", "get_foo", "hello_from_foo"), does_not_raise()),
        (("*",), pytest.raises(AttributeError)),
        (("__add__",), pytest.raises(AttributeError)),
        (("some_fake_method",), pytest.raises(AttributeError)),
    ],
)
def test_validate_delegatee_methods(foo_cls, attrs: Iterable[str], context):
    """Test for delegatee `_validate_delegatee_methods` method"""
    delegatee_cls = foo_cls  # Foo

    with context:
        assert delegatee._validate_delegatee_methods(delegatee_cls, attrs) is None


def test_iter(foo_cls):
    """Test __iter__ method"""
    attrs = ("__len__", "a", "get_foo", "hello_from_foo")
    d = delegatee(foo_cls, attrs=attrs)
    assert list(d) == list(attrs)
