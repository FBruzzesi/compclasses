from __future__ import annotations

from abc import ABCMeta
from typing import Any, Callable, Dict, Iterable, Optional, Tuple, Type, Union

from compclasses._core import generate_properties
from compclasses._delegatee import delegatee
from compclasses._logging import logger


class CompclassMeta(ABCMeta):
    """
    Metaclass that adds class attributes/methods from `delegates` to `clsname` object as
    class properties.


    """

    def __new__(
        cls: Type,
        clsname: str,
        bases: Tuple[Type, ...],
        attrs: Dict[str, Any],
        delegates: Dict[str, Union[Iterable[str], delegatee]],
        verbose: Optional[bool] = True,
        log_func: Callable[[str], None] = logger.info,
    ) -> CompclassMeta:
        """
        Arguments:
            cls: metaclass
            clsname: class name
            bases: base classes
            attrs: class attributes
            delegates: key-value pair of delegates.

                - key: name of the class/instance attribute to which the delegate instance is
                    assigned to.
                - value: must be either a sequence/iterable of method names or a `delegatee`
                    instance. They represent the attributes/methods to forward.

            verbose: defines the level of verbosity when setting those forwarded methods.
            log_func: function to use for logging, if verbose is set to True.
        """

        for _name, _to_inject in generate_properties(delegates, verbose, log_func):
            attrs[_name] = _to_inject

        return super().__new__(cls, clsname, bases, attrs)
