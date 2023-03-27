from importlib import metadata

from ._delegatee import delegatee
from .compclass import compclass
from .metaclass import CompclassMeta

__title__ = __name__
__version__ = metadata.version(__title__)

__all__ = ("compclass", "CompclassMeta", "delegatee")
