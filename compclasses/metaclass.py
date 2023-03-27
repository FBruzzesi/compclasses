from abc import ABCMeta
from typing import Callable, Dict, Iterable, Union

from compclasses._delegatee import delegatee
from compclasses._utils import Verbose, generate_properties, logger


class CompclassMeta(ABCMeta):
    def __new__(
        self,
        _cls,
        bases,
        attrs,
        delegates: Dict[str, Union[Iterable[str], delegatee]],
        verbose: Union[Verbose, int] = Verbose.SILENT,
        log_func: Callable[[str], None] = logger.info,
    ):

        for _name, _to_inject in generate_properties(delegates, verbose, log_func):
            attrs[_name] = _to_inject

        return type(_cls, bases, attrs)
