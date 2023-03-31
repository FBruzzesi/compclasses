from operator import attrgetter
from typing import Callable, Dict, Generator, Iterable, Optional, Tuple, TypeVar, Union

from compclasses._delegatee import delegatee
from compclasses._logging import logger

T = TypeVar("T")


def property_from_delegator(
    delegatee_cls_name: str,
    attr_name: str,
    new_attr_name: str,
) -> property:
    """
    Defines a property called `new_attr_name` based upon `delegate_cls_name.attr_name`.

    This function is used to create a property which will be injected in the class which
    has a delegatee attribute called `delegatee_cls_name` which has an attribute/method
    called `attr_name`.

    Remark that we don't check here if the delegatee has attr_name implemented,
    as delegatee_cls_name only represent the attribute name to which we delegate.

    We define the property as follows:

        - fget: returns the value of delegatee_cls_name.attr_name
        - fset: sets the value of delegatee_cls_name.new_attr_name
        - fdel: deletes the value of delegatee_cls_name.new_attr_name

    and using `wrapped_delegatee = attrgetter(delegatee_cls_name)` which allows us to
    access `self.delegatee_cls_name` by calling  `wrapped_delegatee(self)`.

    Arguments:
        delegatee_cls_name: name of the attribute from which we forward the method.
        attr_name: attribute/method of delegatee_cls_name which we want to forward.
        new_attr_name: name of the new attribute to be created in the scope of the class
            which will be used to access the attribute/method of delegatee_cls.

    Returns:
        property: property which will be injected in the class.
    """

    wrapped_delegatee = attrgetter(
        delegatee_cls_name
    )  # => wrapped_delegatee(self) returns self.delegatee_cls_name

    def fget(self):
        """function to be used for getting an attribute value"""
        return getattr(wrapped_delegatee(self), attr_name)

    def fset(self, value):
        """function to be used for setting an attribute value"""
        setattr(wrapped_delegatee(self), new_attr_name, value)

    def fdel(self):
        """function to be used for deleting an attribute value"""
        delattr(wrapped_delegatee(self), new_attr_name)

    return property(fget=fget, fset=fset, fdel=fdel, doc=fget.__doc__)


def generate_properties(
    delegates: Dict[str, Union[Iterable[str], delegatee]],
    verbose: Optional[bool] = True,
    log_func: Callable[[str], None] = logger.info,
) -> Generator[Tuple[str, property], None, None]:
    """
    Creates a generator of (`new_attr_name`, `property_to_inject`), which is used to
    inject the property into the class of interest, by iterating over the delegates
    argument.

    Arguments:
        delegates: key-value pair of delegates.
        verbose: whether to log the injection of the properties.
        log_func: function used to log, unused if verbose is set to False.

    Returns:
        Generator[Tuple[str, property], None, None]: generator of (`new_attr_name`,
            `property_to_inject`) which is used to inject the property into the class of
            interest.
    """

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

            new_attr_name = f"{pfx}{attr_name}{sfx}"

            property_to_inject = property_from_delegator(
                delegatee_cls_name=delegatee_name,
                attr_name=attr_name,
                new_attr_name=new_attr_name,
            )

            if verbose:
                log_func(f"Setting {new_attr_name} from {delegatee_name}.{attr_name}")

            yield new_attr_name, property_to_inject
