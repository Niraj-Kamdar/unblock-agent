from .getDomainInfo import function as _getDomainInfo
from .signerAddress import function as _signerAddress
from .toEth import function as _toEth
from .toWei import function as _toWei

general = [
    _getDomainInfo,
    _signerAddress,
    _toEth,
    _toWei,
]

__all__ = [
    "general",
]