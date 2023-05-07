import pytest

from compclasses._core import generate_properties
from compclasses._delegatee import delegatee


@pytest.mark.parametrize(
    "attrs",
    [
        ("a",),
        ("a", "_foo"),
        ("a", "_foo", "get_foo"),
        ("a", "_foo", "get_foo", "hello_from_foo"),
        ("a", "_foo", "get_foo", "hello_from_foo", "__len__"),
    ],
)
@pytest.mark.parametrize("pfx", ["", "get_", "get"])
@pytest.mark.parametrize(
    "sfx",
    [
        "",
        "_from_foo",
    ],
)
def test_generate_properties(capsys, foo_cls, attrs, pfx, sfx):
    """Test for generate_properties function"""
    verbose = True
    log_func = print

    property_generator = generate_properties(
        delegates={
            "foo": delegatee(foo_cls, attrs, pfx, sfx, validate=True),
        },
        verbose=verbose,
        log_func=log_func,
    )

    for new_attr_name, _to_inject in property_generator:
        assert isinstance(_to_inject, property)

        if not delegatee._is_dunder_method(new_attr_name):
            assert new_attr_name.startswith(pfx) and new_attr_name.endswith(sfx)
        else:
            assert new_attr_name.startswith("__") and new_attr_name.endswith("__")

        sys_out = capsys.readouterr().out
        assert f"Setting {new_attr_name}" in sys_out
