import logging
from enum import IntEnum
from itertools import filterfalse, tee
from operator import attrgetter
from typing import Callable, Sequence, Type

logger = logging.getLogger("__main__")
logger.setLevel(logging.INFO)


class Verbose(IntEnum):
    """Verbose level class"""

    SILENT = 0
    SET = 1
    GET = 2
    DEL = 3
    ALL = 4


def _property_from_delegator(
    orig_cls: Type,
    delegatee_cls: str,
    attr_name: str,
    prefix: str = "",
    suffix: str = "",
    verbose: Verbose = Verbose.SILENT,
):
    """
    Define a property `{prefix}{attr_name}{suffix}` in the `orig_cls` scope to access as
    `self.<{prefix}{attr_name}{suffix}>` instead of `self.<delegatee_cls>.<attr_name>`.

    Arguments:
        orig_cls: original class
        delegatee_cls: original class attribute from which attr_name has to be forwarded
        attr_name: attribute/method of delegatee_cls which we want to forward
        prefix: prefix of new method
        suffix: suffix of new method
        verbose: verbosity level
    """
    wrapped_delegatee = attrgetter(delegatee_cls)

    if verbose in (1, 4):
        logger.info(
            f"Setting {prefix}{attr_name}{suffix} from {delegatee_cls}.{attr_name}"
        )

    def fget(self):

        if verbose in (2, 4):
            logger.info(
                f"Calling {prefix}{attr_name}{suffix} from {delegatee_cls}.{attr_name}"
            )

        return getattr(wrapped_delegatee(self), attr_name)

    def fset(self, value):
        return setattr(wrapped_delegatee(self), f"{prefix}{attr_name}{suffix}", value)

    def fdel(self):
        if verbose in (3, 4):
            logger.info(
                f"Deleting {prefix}{attr_name}{suffix} from {delegatee_cls}.{attr_name}"
            )

        return delattr(wrapped_delegatee(self), f"{prefix}{attr_name}{suffix}")

    def doc(self):
        return getattr(wrapped_delegatee(self), "__doc__")

    setattr(orig_cls, f"{prefix}{attr_name}{suffix}", property(fget, fset, fdel, doc))


def partition(pred: Callable, iterable: Sequence):
    """
    Use a predicate to partition entries into True entries and False entries
    """
    t1, t2 = tee(iterable)
    return tuple(filter(pred, t1)), tuple(filterfalse(pred, t2))
