from typing import Any, Tuple

import pytest

from compclasses import CompclassMeta, delegatee


def has_all_attrs(cls: Any, attrs: Tuple[str], prefix: str, suffix: str):
    """Checks that cls has all attributes in attrs"""
    for attr in attrs:
        attr_name = attr if delegatee._is_dunder_method(attr) else f"{prefix}{attr}{suffix}"
        assert hasattr(cls, attr_name)


@pytest.mark.parametrize(
    "foo_attrs",
    [("__len__",), ("get_foo", "a"), ("__len__", "get_foo", "hello_from_foo")],
)
@pytest.mark.parametrize(
    "bar_attrs",
    [
        ("__bool__",),
        ("b",),
        (
            "b",
            "__bool__",
        ),
    ],
)
@pytest.mark.parametrize("foo_prefix, foo_suffix", [("foo_pfx_", ""), ("", "_foo_sfx")])
@pytest.mark.parametrize("bar_prefix, bar_suffix", [("bar_pfx_", ""), ("", "_bar_sfx")])
def test_meta(
    foo_cls,
    bar_cls,
    foo_attrs: Tuple[str],
    bar_attrs: Tuple[str],
    foo_prefix: str,
    foo_suffix: str,
    bar_prefix: str,
    bar_suffix: str,
):
    """Test for CompclassMeta metaclass"""
    Foo = foo_cls
    Bar = bar_cls
    delegates = {
        "foo": delegatee(
            delegatee_cls=Foo,
            attrs=foo_attrs,
            prefix=foo_prefix,
            suffix=foo_suffix,
            validate=True,
        ),
        "bar": delegatee(
            delegatee_cls=Bar,
            attrs=bar_attrs,
            prefix=bar_prefix,
            suffix=bar_suffix,
            validate=True,
        ),
    }

    class Baz_composed(metaclass=CompclassMeta, delegates=delegates):
        """Baz composed class using metaclass"""

        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar

    has_all_attrs(Baz_composed, foo_attrs, foo_prefix, foo_suffix)
    has_all_attrs(Baz_composed, bar_attrs, bar_prefix, bar_suffix)

    # Check instance
    foo_obj = foo_cls(value=111)
    bar_obj = bar_cls()

    baz_obj: Baz_composed = Baz_composed(foo_obj, bar_obj)

    has_all_attrs(baz_obj, foo_attrs, foo_prefix, foo_suffix)
    has_all_attrs(baz_obj, bar_attrs, bar_prefix, bar_suffix)
