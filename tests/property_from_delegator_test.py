from typing import Tuple

import pytest

from compclasses.compclass import _property_from_delegator


@pytest.mark.parametrize(
    "attr_name, prefix, suffix, method_args",
    [
        ("get_foo", "", "", tuple()),
        ("get_foo", "", "_from_foo_cls", tuple()),
        ("hello_from_foo", "", "_from_foo_cls", ("GitHub",)),
        ("__len__", "", "", tuple()),
    ],
)
def test_property_from_delegator(
    foo_cls, bar_cls, attr_name: str, prefix: str, suffix: str, method_args: Tuple
):
    """Test for property_from_delegator function"""

    foo_obj = foo_cls(value=111)
    delegatee_cls_name = "foo"
    new_attr_name = f"{prefix}{attr_name}{suffix}"

    Bar = bar_cls

    _property_from_delegator(
        orig_cls=Bar,
        delegatee_cls_name=delegatee_cls_name,
        attr_name=attr_name,
        prefix=prefix,
        suffix=suffix,
    )

    bar_obj = Bar(foo_obj)

    assert hasattr(Bar, new_attr_name)
    assert getattr(bar_obj, new_attr_name)(*method_args) == getattr(foo_obj, attr_name)(
        *method_args
    )

    delattr(Bar, new_attr_name)
    assert not hasattr(Bar, new_attr_name)


@pytest.mark.parametrize("attr_name", ["a"])
def test_property_from_delegator_logs(caplog, foo_cls, bar_cls, attr_name: str):
    """Test for property_from_delegator function"""

    foo_obj = foo_cls(value=111)
    delegatee_cls_name = "foo"
    Bar = bar_cls

    _property_from_delegator(
        orig_cls=Bar,
        delegatee_cls_name=delegatee_cls_name,
        attr_name=attr_name,
        verbose=4,
    )
    assert f"Setting {attr_name} from {delegatee_cls_name}.{attr_name}" in caplog.text

    bar_obj = Bar(foo_obj)

    _ = getattr(bar_obj, attr_name)
    assert f"Calling {attr_name} from {delegatee_cls_name}.{attr_name}" in caplog.text
