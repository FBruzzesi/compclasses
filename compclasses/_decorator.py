from typing import Callable, Dict, Iterable, Optional, Type, TypeVar, Union

from compclasses._core import generate_properties, logger
from compclasses._delegatee import delegatee

T = TypeVar("T")


def compclass(
    _cls: Optional[Type[T]] = None,
    delegates: Optional[Dict[str, Union[Iterable[str], delegatee]]] = None,
    verbose: Optional[bool] = True,
    log_func: Callable[[str], None] = logger.info,
) -> Union[
    Type[T], Callable[[Type[T], Dict[str, Union[Iterable[str], delegatee]]], Type[T]]
]:
    """
    Decorator that adds class attributes/methods from `delegates` to `_cls` object as
    class properties.

    Arguments:
        _cls: class to which attributes/methods should be forwarded to.
        delegates: key-value pair of delegates.

            - key: name of the class/instance attribute to which the delegate instance is
                assigned to.
            - value: must be either a sequence/iterable of method names or a `delegatee`
                instance. They represent the attributes/methods to forward.

        verbose: defines the level of verbosity when setting those forwarded methods.
        log_func: function to use for logging, if verbose is set to True.

    Raises:
        ValueError: `delegates` param cannot be `None`

    Returns:
        Class with added methods from delegates.

    Usage:

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
    """
    if delegates is None:
        raise ValueError("`delegates` param cannot be `None`")

    def wrap(
        _cls: Type[T],
        delegates: Dict[str, Union[Iterable[str], delegatee]] = delegates,  # type: ignore
    ) -> Type[T]:

        for _name, _to_inject in generate_properties(delegates, verbose, log_func):
            setattr(_cls, _name, _to_inject)

        return _cls

    if _cls is None:
        # Called with parens: @compclass(delegates=...)
        return wrap

    # Called directly on class C = compclass(C, delegates)
    return wrap(_cls)
