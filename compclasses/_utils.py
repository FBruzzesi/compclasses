from enum import IntEnum
from operator import attrgetter
from typing import Callable, Dict, Iterable, TypeVar, Union

from compclasses._delegatee import delegatee
from compclasses._logging import logger

T = TypeVar("T")


class Verbose(IntEnum):
    """Verbose level class"""

    SILENT = 0
    SET = 1
    GET = 2
    DEL = 3
    ALL = 4


def property_from_delegator(
    delegatee_cls_name: str,
    attr_name: str,
    prefix: str = "",
    suffix: str = "",
    verbose: Union[Verbose, int] = Verbose.SILENT,
    log_func: Callable[[str], None] = logger.info,
) -> property:
    """
    Defines a property `{prefix}{attr_name}{suffix}` in the `orig_cls` scope to access as
    `self.<{prefix}{attr_name}{suffix}>` instead of `self.<delegatee_cls>.<attr_name>`.

    Remark that we don't check here if the delegatee has the passed attribute,
    as delegatee_cls_name only represent the cls attribute name to which the
    delegatee is assigned.

    Arguments:
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
            log_func(f"Deleting {prefix}{attr_name}{suffix}")
        return delattr(wrapped_delegatee(self), attr_name)

    # orig_cls.<{prefix}{attr_name}{suffix}> = property(...)
    return property(fget=fget, fset=fset, fdel=fdel, doc=fget.__doc__)


def generate_properties(
    delegates: Dict[str, Union[Iterable[str], delegatee]],
    verbose: Union[Verbose, int] = Verbose.SILENT,
    log_func: Callable[[str], None] = logger.info,
):
    """
    Generates an iterable of (name, property) to be injected in the class
    """

    # rewrite the following code to return an iterable of (name, property)
    # instead of injecting them directly in the class

    for delegatee_name, delegatee_instance in delegates.items():

        is_delegatee = isinstance(delegatee_instance, delegatee)

        for attr_name in delegatee_instance:

            if is_delegatee and not delegatee._is_dunder_method(attr_name):
                pfx, sfx = (
                    delegatee_instance._prefix,  # type: ignore
                    delegatee_instance._suffix,  # type: ignore
                )
            else:
                pfx, sfx = "", ""

            name = f"{pfx}{attr_name}{sfx}"
            property_to_inject = property_from_delegator(
                delegatee_cls_name=delegatee_name,
                attr_name=attr_name,
                prefix=pfx,  # type: ignore
                suffix=sfx,  # type: ignore
                verbose=verbose,
                log_func=log_func,
            )

            yield name, property_to_inject
