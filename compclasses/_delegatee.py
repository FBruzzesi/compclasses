import inspect
import re
from itertools import filterfalse, tee
from typing import Callable, Iterable, Optional, Tuple, Type, TypeVar

from compclasses._logging import logger

T = TypeVar("T")


def partition(
    pred: Callable[[T], bool], iterable: Iterable[T]
) -> Tuple[Tuple[T, ...], Tuple[T, ...]]:
    """
    Use a predicate to partition entries into True and False entries.

    Arguments:
        pred: function used to test each element in the iterable, returning True or False.
        iterable: An iterable of items to be partitioned according to the predicate
            result of each item.

    Returns:
        A tuple of two tuples. The first tuple contains all items for which pred(item) is
            True, and the second tuple contains all items for which pred(item) is False.
    """

    t1, t2 = tee(iterable)
    return tuple(filter(pred, t1)), tuple(filterfalse(pred, t2))


class delegatee:
    """
    Delegatee class, used in place of an iterable when defining delegates dictionary.

    This class provides the following features:

    - It allows to validate the delegatee class attributes/methods.
    - It supports the "*" argument in attrs parameter, which automatically detects all
        non-dunder methods of the delegatee class.
    - It enables adding prefix and/or suffix to non-dunder methods.

    Arguments:
        delegatee_cls: class from which we delegate. This is the class/type definition,
            there is no need to instantiate it.
        attrs: sequence of attributes/methods to inject on the composed class.
            Remark that if "*" is present, we inject all the methods, excluding dunder
            methods which need to be explicitly stated.
        prefix: injected methods prefix, unused for dunder methods.
        suffix: injected methods suffix, unused for dunder methods.
        validate: whether or not to validate if `delegatee_cls` has all the methods
            and/or attributes.

            Remark that:

            - Methods are searched in class definition `__dict__`.
            - Attributes are searched in class `__init__` code by matching the following
                regex: `"self.{attr}"` (more technically, `re.compile(r"self.(\w+)")`).

    Methods:
        - _parse_attrs: parses the original attrs sequence, splitting between
            dunder and class methods.
        - _is_dunder_method: assess whether or not an attribute is a dunder
            method.
        - _validate_delegatee_methods: checks if delegatee_cls has all
            attributes/methods in attrs.
    """

    def __init__(
        self,
        delegatee_cls: Type,
        attrs: Iterable[str],
        prefix: Optional[str] = "",
        suffix: Optional[str] = "",
        validate: Optional[bool] = True,
    ):

        if not attrs:  # empty iterable such as list(), tuple(), None, etc...
            raise ValueError("attrs parameter cannot be None")

        self.delegatee_cls = delegatee_cls

        if delegatee_cls is not None:
            self._attrs = self._parse_attrs(delegatee_cls, attrs)
        else:
            self._attrs = tuple(attrs)

        if validate and (delegatee_cls is not None):
            self._validate_delegatee_methods(self.delegatee_cls, self._attrs)

        self._prefix = prefix
        self._suffix = suffix

    def __iter__(self):
        for attr_name in self._attrs:
            yield attr_name

    @staticmethod
    def _parse_attrs(delegatee_cls: Type, attrs: Iterable[str]) -> Tuple[str, ...]:
        """
        Parses the original attrs sequence:

        - Splits between dunder and class methods.
        - If "*" is present, we add all the methods to the list of methods to inject,
            excluding dunder methods which need to be explicitly stated.
        - If "*" is not present, we simply return the original attrs sequence.
        """

        dunder_methods, base_methods = partition(delegatee._is_dunder_method, attrs)
        if "*" in base_methods:
            pattern = re.compile(r"self.(\w+)")

            methods = tuple(
                attr_name
                for attr_name in delegatee_cls.__dict__.keys()
                if not delegatee._is_dunder_method(attr_name)
            )
            try:
                co_code = inspect.getsource(delegatee_cls.__init__)
                init_attrs = tuple(pattern.findall(co_code))

            except Exception as e:
                logger.info(
                    f"Unable to parse __init__ method of {delegatee_cls} due to error: {e}"
                )
                init_attrs = tuple()

            all_methods = methods + init_attrs
        else:
            all_methods = base_methods
        return dunder_methods + all_methods

    @staticmethod
    def _is_dunder_method(attr_name: str) -> bool:
        """
        Assesses whether or not `attr_name` is a dunder method by checking if it starts
        and ends with "__".
        """
        return attr_name.startswith("__") and attr_name.endswith("__")

    @staticmethod
    def _validate_delegatee_methods(delegatee_cls: Type, attrs: Iterable[str]) -> None:
        """
        Checks if delegatee_cls has all attributes and methods listed in attrs

        Arguments:
            delegatee_cls: class from which we delegate. This is the class definition,
                there is no need to instantiate it.
            attrs: sequence of attributes/methods to inject on the composed class.

        Raises:
            AttributeError: if delegatee_cls has no attribute/method in attrs.
        """

        cls_methods = tuple([a[0] for a in inspect.getmembers(delegatee_cls)])

        try:
            co_code = inspect.getsource(delegatee_cls.__init__)
            pattern = re.compile(r"self.(\w+)")
            init_attrs = tuple(pattern.findall(co_code))

        except Exception as e:
            logger.info(
                f"Unable to parse __init__ method of {delegatee_cls} due to error: {e}"
            )
            init_attrs = tuple()

        all_methods = cls_methods + init_attrs
        for attr_name in attrs:
            if attr_name not in all_methods:
                raise AttributeError(
                    f"'{delegatee_cls}' has no attribute nor method '{attr_name}'"
                )
