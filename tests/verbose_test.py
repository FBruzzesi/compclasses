import pytest

from compclasses.compclass import Verbose


@pytest.mark.parametrize(
    "verbose_level, expected",
    [
        (Verbose.SILENT, 0),
        (Verbose.SET, 1),
        (Verbose.GET, 2),
        (Verbose.DEL, 3),
        (Verbose.ALL, 4),
    ],
)
def test_verbose_cls(verbose_level, expected: int):
    """Test for Verbose class"""
    assert verbose_level == expected
