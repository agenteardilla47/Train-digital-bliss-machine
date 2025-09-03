"""
Cryptographic Obliteration for Source Material Destruction

This module implements Phase 2 of the CF protocol: securely deleting
all source-correlated structures using forward-secure key erasure.
"""

from .cryptographic_obliterator import CryptographicObliterator
from .tee_support import TEESupport

__all__ = [
    "CryptographicObliterator",
    "TEESupport"
]