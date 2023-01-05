from typing import Any, Iterable, Tuple

import pytest

from compclasses.compclass import partition


def is_even(x: int) -> bool:
    """Returns True if an integer is even"""
    return x % 2 == 0


@pytest.mark.parametrize(
    "iterable, expected",
    [
        ([1, 2, 3, 4], ((2, 4), (1, 3))),
        ([], ((), ())),
    ],
)
def test_partition(iterable: Iterable, expected: Tuple[Any, ...]):
    """Test for partition function"""
    assert partition(pred=is_even, iterable=iterable) == expected
