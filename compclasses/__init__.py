from importlib import metadata

from .compclass import compclass, delegatee

__title__ = __name__
__version__ = metadata.version(__title__)

__all__ = ("compclass", "delegatee")
