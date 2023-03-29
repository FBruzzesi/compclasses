from importlib import metadata

from compclasses._delegatee import delegatee
from compclasses.compclass import compclass
from compclasses.metaclass import CompclassMeta

__title__ = __name__
__version__ = metadata.version(__title__)

__all__ = ("compclass", "CompclassMeta", "delegatee")
