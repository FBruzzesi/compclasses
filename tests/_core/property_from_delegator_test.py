import pytest

from compclasses._core import property_from_delegator


@pytest.mark.parametrize(
    "attr_name, pfx, sfx, method_args",
    [
        ("__len__", "", "", tuple()),
        ("get_foo", "", "", tuple()),
        ("get_foo", "", "_from_foo_cls", tuple()),
        ("hello_from_foo", "", "_from_foo_cls", ("GitHub",)),
    ],
)
def test_property_from_delegator(foo_cls, bar_cls, baz_cls, attr_name, pfx, sfx, method_args):
    """Test for property_from_delegator function"""
    foo_obj = foo_cls(value=111)
    bar_obj = bar_cls()

    new_attr_name = f"{pfx}{attr_name}{sfx}"
    _property_to_inject = property_from_delegator("foo", attr_name, new_attr_name)

    Baz = baz_cls
    assert not hasattr(Baz, new_attr_name)

    setattr(Baz, new_attr_name, _property_to_inject)
    baz_obj = Baz(foo_obj, bar_obj)

    assert hasattr(Baz, new_attr_name)
    assert hasattr(baz_obj, new_attr_name)
    assert getattr(baz_obj, new_attr_name)(*method_args) == getattr(foo_obj, attr_name)(*method_args)

    setattr(baz_obj, new_attr_name, _property_to_inject)
    delattr(Baz, new_attr_name)  # can't delete from instance, only from class!!!

    assert not hasattr(baz_obj, new_attr_name)
