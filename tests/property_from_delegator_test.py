from typing import Tuple

import pytest

from compclasses._utils import property_from_delegator


@pytest.mark.parametrize(
    "attr_name, prefix, suffix, method_args",
    [
        ("__len__", "", "", tuple()),
        ("get_foo", "", "", tuple()),
        ("get_foo", "", "_from_foo_cls", tuple()),
        ("hello_from_foo", "", "_from_foo_cls", ("GitHub",)),
    ],
)
def test_property_from_delegator(
    foo_cls,
    bar_cls,
    baz_cls,
    attr_name: str,
    prefix: str,
    suffix: str,
    method_args: Tuple,
):
    """Test for property_from_delegator function"""

    foo_obj = foo_cls(value=111)
    bar_obj = bar_cls()
    delegatee_cls_name = "foo"
    new_attr_name = f"{prefix}{attr_name}{suffix}"

    Baz = baz_cls

    assert not hasattr(Baz, new_attr_name)

    _name = f"{prefix}{attr_name}{suffix}"
    _property = property_from_delegator(
        delegatee_cls_name=delegatee_cls_name,
        attr_name=attr_name,
        prefix=prefix,
        suffix=suffix,
    )
    setattr(Baz, _name, _property)

    baz_obj = Baz(foo_obj, bar_obj)

    assert hasattr(baz_obj, new_attr_name)
    assert getattr(baz_obj, new_attr_name)(*method_args) == getattr(foo_obj, attr_name)(
        *method_args
    )

    delattr(Baz, new_attr_name)
    assert not hasattr(Baz, new_attr_name)


@pytest.mark.parametrize("attr_name", ["a"])
def test_property_from_delegator_logs(caplog, foo_cls, bar_cls, baz_cls, attr_name: str):
    """Test for property_from_delegator function"""

    foo_obj = foo_cls(value=111)
    bar_obj = bar_cls()
    delegatee_cls_name = "foo"

    Baz = baz_cls

    _name = f"{attr_name}"
    _property = property_from_delegator(
        delegatee_cls_name=delegatee_cls_name,
        attr_name=attr_name,
        verbose=4,
    )
    setattr(Baz, _name, _property)

    assert f"Setting {attr_name} from {delegatee_cls_name}.{attr_name}" in caplog.text

    baz_obj = Baz(foo_obj, bar_obj)

    _ = getattr(baz_obj, attr_name)
    assert f"Calling {attr_name} from {delegatee_cls_name}.{attr_name}" in caplog.text

    delattr(Baz, attr_name)
