from .getDomainInfo import function as _getDomainInfo
from .signerAddress import function as _signerAddress

general = [
    _getDomainInfo,
    _signerAddress,
]

__all__ = [
    "general",
]