import inspect
import logging
from enum import IntEnum
from itertools import filterfalse, tee
from operator import attrgetter
from typing import Any, Callable, Dict, Iterable, Optional, Tuple, Type, Union

logging.basicConfig(format="%(message)s", level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Verbose(IntEnum):
    """Verbose level class"""

    SILENT = 0
    SET = 1
    GET = 2
    DEL = 3
    ALL = 4


def partition(
    pred: Callable[..., bool], iterable: Iterable
) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    """
    Use a predicate to partition entries into True entries and False entries
    """
    t1, t2 = tee(iterable)
    return tuple(filter(pred, t1)), tuple(filterfalse(pred, t2))


class delegatee:
    """
    Base delegatee class, used in place of an iterable when defining delegates.

    This class provides the following features:

    - It allows to validate the delegatee class attributes/methods
    - It supports the "*" argument in attrs param, which automatically detects
        all non-dunder methods/attributes
    - It enables adding prefix and/or suffix to non-dunder methods/attributes

    Arguments:
        delegatee_cls: class from which we delegate.
            This is the class/type definition.
        attrs: sequence of attributes/methods to inject on the composed class.
            Remark that if "*" is present, we inject all the methods,
            excluding dunder methods which need to be explicitly stated.
        prefix: injected method prefix, unused with dunder methods
        suffix: injected method suffix, unused with dunder methods
        validate: whether or not to validate if delegatee_cls has all the attrs.

            Remark that validate function includes methods and class attributes
            only, it doesn't detect instance attributes, therefore if instance
            attributes are passed and validate param is True then the check will
            fail.

    Methods:
        - _parse_attrs: parses the original attrs sequence, splitting between
            dunder and class methods.
        - _is_dunder_method: assess whether or not an attribute is a dunder
            method.
        - _validate_delegatee_methods: checks if delegatee_cls has all
            attributes/methods in attrs
    """

    def __init__(
        self,
        delegatee_cls: Type[Any],
        attrs: Iterable[str],
        prefix: str = "",
        suffix: str = "",
        validate: bool = True,
    ):

        if attrs is None:
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
        """Parses the original attrs sequence"""

        dunder_methods, cls_methods = partition(delegatee._is_dunder_method, attrs)
        if "*" in cls_methods:
            all_methods = tuple(
                attr_name
                for attr_name in delegatee_cls.__dict__.keys()
                if not delegatee._is_dunder_method(attr_name)
            )
        else:
            all_methods = cls_methods
        return dunder_methods + all_methods

    @staticmethod
    def _is_dunder_method(attr_name: str) -> bool:
        """Assess whether or not attr_name is a dunder method"""
        return attr_name.startswith("__") and attr_name.endswith("__")

    @staticmethod
    def _validate_delegatee_methods(
        delegatee_cls: Type[Any], attrs: Iterable[str]
    ) -> None:
        """Checks if delegatee_cls has all attributes/methods in attrs"""

        cls_attrs_methods = tuple(delegatee_cls.__dict__.keys())
        cls_attrs_methods = tuple([a[0] for a in inspect.getmembers(delegatee_cls)])
        # Remark: includes methods and class attributes only
        #     it doesn't detect instance attributes!!!

        for attr_name in attrs:
            if attr_name not in cls_attrs_methods:
                raise AttributeError(
                    f"'{delegatee_cls}' has no attribute/method '{attr_name}'"
                )


def compclass(
    cls: Optional[Type[Any]] = None,
    delegates: Optional[Dict[str, Union[Iterable[str], delegatee]]] = None,
    verbose: Union[Verbose, int] = Verbose.SILENT,
    log_func: Callable[[str], None] = logger.info,
) -> Union[Callable[[Any], Type[Any]], Type[Any]]:
    """
    Adds class attributes/methods from `delegates` to `cls` object as class properties.

    `delegates` dictionary consists of key-value pair, of the following form.
    The key corresponds to the name of the cls attribute to which the delegate
    instance is assigned to.
    The value should be an iterable or `delegatee` instance with the name of the
    attributes/methods to forward.

    `verbose` defines the level of verbosity when setting-calling-deleting those
    forwarded methods.

    The function can be used as a class decorator:

    ```python
    class Foo:
        a = 1

        def __len__(self) -> int:
            # custom len method
            return 42

    @compclass(delegates={"_foo": ("a", "__len__")})
    class Bar:
        def __init__(self, foo: Foo):
            self._foo = foo

    foo = Foo()
    bar = Bar(foo)

    bar.a  # -> 1 (instead of bar._foo.a)
    len(bar)  # -> 42 (instead of len(bar._foo))
    ```

    Arguments:
        cls: class to which attributes/methods should be forwarded to.
        delegates: key-value pair of delegates.

            - key: name of the cls attribute to which the delegate instance is
                assigned to.
            - value: must be either a sequence of method names or a delegatee
                instance.

        verbose: defines the level of verbosity (0-4) when setting-calling-deleting
            forwarded methods.

            - 0: SILENT
            - 1: SET
            - 2: GET
            - 3: DEL
            - 4: ALL

        log_func: function used to log, unused if verbose = 0

    Raises:
        ValueError: `delegates` param cannot be `None`

    Returns:
        Type[Any]: class with added methods from delegates
    """
    if delegates is None:
        raise ValueError("`delegates` param cannot be `None`")

    def wrap(
        cls: Type[Any],
        delegates: Dict[str, Union[Iterable[str], delegatee]] = delegates,
    ) -> Type[Any]:

        for delegatee_name, delegatee_instance in delegates.items():

            # TODO: Do we even want this feature?
            # This only make sense if one has the same delegator instance all the time!
            # if not isinstance(delegatee_instance.delegatee_cls, type):
            #     setattr(cls, delegatee_name, delegatee_instance.delegatee_cls)

            is_delegatee = isinstance(delegatee_instance, delegatee)

            for attr_name in delegatee_instance:

                if is_delegatee and not delegatee._is_dunder_method(attr_name):
                    pfx, sfx = (
                        delegatee_instance._prefix,
                        delegatee_instance._suffix,
                    )
                else:
                    pfx, sfx = "", ""

                property_from_delegator(
                    orig_cls=cls,
                    delegatee_cls_name=delegatee_name,
                    attr_name=attr_name,
                    prefix=pfx,
                    suffix=sfx,
                    verbose=verbose,
                    log_func=log_func,
                )

        return cls

    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @compclass without parens.
    # This case should never happen as delegates param cannot be None.
    return wrap(cls)


def property_from_delegator(
    orig_cls: Type,
    delegatee_cls_name: str,
    attr_name: str,
    prefix: str = "",
    suffix: str = "",
    verbose: Union[Verbose, int] = Verbose.SILENT,
    log_func: Callable[[str], None] = logger.info,
):
    """
    Defines a property `{prefix}{attr_name}{suffix}` in the `orig_cls` scope to access as
    `self.<{prefix}{attr_name}{suffix}>` instead of `self.<delegatee_cls>.<attr_name>`.

    Remark that we don't check here if the delegatee has the passed attribute,
    as delegatee_cls_name only represent the cls attribute name to which the
    delegatee is assigned.

    Arguments:
        orig_cls: original class
        delegatee_cls: original class attribute from which attr_name has to be forwarded
        attr_name: attribute/method of delegatee_cls which we want to forward
        prefix: prefix of new method
        suffix: suffix of new method
        verbose: defines the level of verbosity (0-4) when setting-calling-deleting
            forwarded methods.

            - 0: SILENT
            - 1: SET
            - 2: GET
            - 3: DEL
            - 4: ALL

        log_func: function used to log, unused if verbose = 0
    """

    wrapped_delegatee = attrgetter(
        delegatee_cls_name
    )  # => wrapped_delegatee(self) returns self.delegatee_cls_name

    if verbose in (1, 4):
        log_func(
            f"Setting {prefix}{attr_name}{suffix} from {delegatee_cls_name}.{attr_name}"
        )

    def fget(self):
        """function to be used for getting an attribute value"""
        if verbose in (2, 4):
            log_func(
                f"Calling {prefix}{attr_name}{suffix} from {delegatee_cls_name}.{attr_name}"
            )

        return getattr(wrapped_delegatee(self), attr_name)

    def fset(self, value):
        """function to be used for setting an attribute value"""
        if verbose in (1, 4):
            log_func(f"Setting {prefix}{attr_name}{suffix} to {value}")
        return setattr(wrapped_delegatee(self), attr_name, value)

    def fdel(self):
        """
        function to be used for del'ing an attribute

        Remark:
            This should never work when using delegatee(..., validate=True) as
            only cls methods and cls attributes can be detected, but cannot be
            deleted from an instance
        """

        if verbose in (3, 4):
            log_func(f"Deleting {prefix}{attr_name}{suffix} from {orig_cls.__name__}")
        return delattr(wrapped_delegatee(self), attr_name)

    # orig_cls.<{prefix}{attr_name}{suffix}> = property(...)
    setattr(
        orig_cls,
        f"{prefix}{attr_name}{suffix}",
        property(fget=fget, fset=fset, fdel=fdel, doc=fget.__doc__),
    )
