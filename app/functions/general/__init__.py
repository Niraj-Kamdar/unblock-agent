from .getOwner import function as _getOwner
from .signerAddress import function as _signerAddress

general = [
    _getOwner,
    _signerAddress,
]

__all__ = [
    "general",
]