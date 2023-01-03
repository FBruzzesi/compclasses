import logging
from enum import IntEnum
from itertools import filterfalse, tee
from operator import attrgetter
from typing import Callable, Dict, List, Optional, Sequence, Type, Union

logger = logging.getLogger("__main__")
logger.setLevel(logging.INFO)


class Verbose(IntEnum):
    """Verbose level class"""

    SILENT = 0
    SET = 1
    GET = 2
    DEL = 3
    ALL = 4


class delegatee:
    """Base delegatee class"""

    def __init__(
        self,
        delegatee_cls: Type,
        attrs: Sequence[str],
        prefix: str = "",
        suffix: str = "",
        validate: bool = True,
    ):

        self.delegatee = delegatee_cls
        self._attrs = self._parse_attrs(delegatee_cls, attrs)

        print(self._attrs)
        if validate:
            self._validate_delegatee_methods(self.delegatee, self._attrs)

        self._prefix = prefix
        self._suffix = suffix

    def __iter__(self):
        for attr_name in self._attrs:
            yield attr_name

    @staticmethod
    def _parse_attrs(delegatee_cls, attrs: Sequence[str]) -> List[str]:
        """Parses the original attrs sequence"""

        dunder_methods, cls_methods = partition(delegatee._is_dunder_method, attrs)
        if "*" in cls_methods:
            cls_methods = tuple(
                attr_name
                for attr_name in delegatee_cls.__dict__.keys()
                if attr_name not in dunder_methods
            )

        return dunder_methods + cls_methods

    @staticmethod
    def _is_dunder_method(attr_name: str) -> bool:
        """Assess whether or not attr_name is a dunder method"""
        return attr_name.startswith("__") and attr_name.endswith("__")

    @staticmethod
    def _validate_delegatee_methods(delegatee_cls: Type, attrs: Sequence[str]):
        """Checks if delegatee_cls has all attributes/methods in attrs"""

        cls_attrs_methods = list(delegatee_cls.__dict__.keys())
        # Remark: includes methods and class attributes only, it doesn't detect instance attributes!!!

        for attr_name in attrs:
            if attr_name not in cls_attrs_methods:
                raise AttributeError(
                    f"'{delegatee_cls}' has no attribute/method '{attr_name}'"
                )


def compclass(
    cls=None,
    delegates: Dict[str, Union[Sequence[str], delegatee]] = None,
    verbose: Verbose = Verbose.SILENT,
):
    """
    Adds methods from delegates to cls

    Arguments:
        cls: class to decorate
        delegates: key-value pair of delegates.
            - key must be the class attribute name from which we want to forward methods
            - value must be either a sequence of method names or a delegatee instance
        verbose: verbisity level (0-4)

    Raises:
        ValueError: delegates param cannot be None

    Returns:
        class with added methods from delegates
    """
    if delegates is None:
        raise ValueError("`delegates` cannot be None")

    def wrap(cls):

        for delegatee_name, delegatee_instance in delegates.items():

            for attr_name in delegatee_instance:

                if isinstance(
                    delegatee_instance, delegatee
                ) and not delegatee._is_dunder_method(attr_name):
                    pfx, sfx = delegatee_instance._prefix, delegatee_instance._suffix
                else:
                    pfx, sfx = "", ""

                _property_from_delegator(
                    orig_cls=cls,
                    delegatee_cls=delegatee_name,
                    attr_name=attr_name,
                    prefix=pfx,
                    suffix=sfx,
                    verbose=verbose,
                )

        return cls

    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @compclass without parens.
    return wrap(cls)


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
        """function to be used for getting an attribute value"""
        if verbose in (2, 4):
            logger.info(
                f"Calling {prefix}{attr_name}{suffix} from {delegatee_cls}.{attr_name}"
            )

        return getattr(wrapped_delegatee(self), attr_name)

    def fset(self, value):
        """function to be used for setting an attribute value"""
        if verbose in (1, 4):
            logger.info(f"Setting {prefix}{attr_name}{suffix} to {value}")
        return setattr(wrapped_delegatee(self), f"{prefix}{attr_name}{suffix}", value)

    def fdel(self):
        """function to be used for del'ing an attribute"""
        if verbose in (3, 4):
            logger.info(
                f"Deleting {prefix}{attr_name}{suffix} from {delegatee_cls}.{attr_name}"
            )

        return delattr(wrapped_delegatee(self), f"{prefix}{attr_name}{suffix}")

    def doc(self) -> Optional[str]:
        """docstring"""
        return getattr(wrapped_delegatee(self), attr_name).__doc__

    setattr(orig_cls, f"{prefix}{attr_name}{suffix}", property(fget, fset, fdel, doc))


def partition(pred: Callable[..., bool], iterable: Sequence):
    """
    Use a predicate to partition entries into True entries and False entries
    """
    t1, t2 = tee(iterable)
    return tuple(filter(pred, t1)), tuple(filterfalse(pred, t2))
