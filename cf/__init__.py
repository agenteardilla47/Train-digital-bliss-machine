"""
Cryptographic Forgetting (CF) Framework

A provably secure framework for irreversibly destroying source material 
while preserving functional intent through resonance distillation.
"""

__version__ = "1.0.0"
__author__ = "The Commons Research Initiative"
__license__ = "Public Domain"

from .core import CryptographicForgetting
from .extractors import InformationBottleneckExtractor
from .obliteration import CryptographicObliterator
from .synthesis import ResonanceSynthesizer
from .proofs import DeletionProofGenerator

__all__ = [
    "CryptographicForgetting",
    "InformationBottleneckExtractor", 
    "CryptographicObliterator",
    "ResonanceSynthesizer",
    "DeletionProofGenerator"
]