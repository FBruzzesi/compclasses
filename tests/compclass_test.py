from typing import Any, Dict, Iterable, Tuple, Type, Union

import pytest

from compclasses import compclass, delegatee


def has_all_attrs(cls: Type, attrs: Tuple[str], prefix: str, suffix: str):
    """Checks that cls has all attributes in attrs"""
    for attr in attrs:

        attr_name = (
            attr if delegatee._is_dunder_method(attr) else f"{prefix}{attr}{suffix}"
        )
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
@pytest.mark.parametrize("foo_prefix, foo_suffix", [("foo_pre_", ""), ("", "_foo_sfx")])
@pytest.mark.parametrize("bar_prefix, bar_suffix", [("bar_pre_", ""), ("", "_bar_sfx")])
def test_compclass(
    foo_cls,
    bar_cls,
    baz_cls,
    foo_attrs: Tuple[str],
    bar_attrs: Tuple[str],
    foo_prefix: str,
    foo_suffix: str,
    bar_prefix: str,
    bar_suffix: str,
):
    """Test for compclass decorator"""

    delegates: Dict[str, Union[Iterable[str], delegatee]] = {
        "foo": delegatee(
            delegatee_cls=foo_cls,
            attrs=foo_attrs,
            prefix=foo_prefix,
            suffix=foo_suffix,
            validate=True,
        ),
        "bar": delegatee(
            delegatee_cls=bar_cls,
            attrs=bar_attrs,
            prefix=bar_prefix,
            suffix=bar_suffix,
            validate=True,
        ),
    }

    # Check class definition
    Baz: Type[Any] = compclass(baz_cls, delegates=delegates)

    has_all_attrs(Baz, foo_attrs, foo_prefix, foo_suffix)
    has_all_attrs(Baz, bar_attrs, bar_prefix, bar_suffix)

    # Check instance
    foo_obj = foo_cls(value=111)
    bar_obj = bar_cls()

    baz_obj = Baz(foo_obj, bar_obj)

    has_all_attrs(baz_obj, foo_attrs, foo_prefix, foo_suffix)
    has_all_attrs(baz_obj, bar_attrs, bar_prefix, bar_suffix)


def test_compclass_error(
    baz_cls,
):
    """Test for compclass without delegates"""
    with pytest.raises(ValueError):
        compclass(baz_cls)
