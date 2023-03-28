from abc import ABCMeta
from typing import Callable, Dict, Iterable, Optional, Union

from compclasses._core import generate_properties
from compclasses._delegatee import delegatee
from compclasses._logging import logger


class CompclassMeta(ABCMeta):
    """
    Metaclass for compclass - adds class attributes/methods from `delegates` to `cls`
    object as class properties.

    Arguments:
        `delegates`: dictionary of key-value pair, of the following form:
            - The key corresponds to the name of the cls attribute to which the delegate
            instance is assigned to.
            - The value should be an iterable or `delegatee` instance with the name of
                the attributes/methods to forward.
        `verbose` defines the level of verbosity when setting those forwarded methods.
        `log_func`: function to use for logging, if verbose is set to True.
    """

    def __new__(
        self,
        _cls,
        bases,
        attrs,
        delegates: Dict[str, Union[Iterable[str], delegatee]],
        verbose: Optional[bool] = True,
        log_func: Callable[[str], None] = logger.info,
    ):

        for _name, _to_inject in generate_properties(delegates, verbose, log_func):
            attrs[_name] = _to_inject

        return type(_cls, bases, attrs)
