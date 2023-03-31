from importlib import metadata

from ._decorator import compclass
from ._delegatee import delegatee
from ._meta import CompclassMeta

__title__ = __name__
__version__ = metadata.version(__title__)

__all__ = ("compclass", "CompclassMeta", "delegatee")
