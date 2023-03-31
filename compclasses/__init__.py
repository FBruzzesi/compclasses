from importlib import metadata

from compclasses._decorator import compclass
from compclasses._delegatee import delegatee
from compclasses._meta import CompclassMeta

__title__ = __name__
__version__ = metadata.version(__title__)

__all__ = ("compclass", "CompclassMeta", "delegatee")
