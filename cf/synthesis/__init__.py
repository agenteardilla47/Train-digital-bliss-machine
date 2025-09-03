"""
Resonance Synthesis for Output Generation

This module implements Phase 3 of the CF protocol: generating outputs
from distilled resonance plus fresh cryptographic entropy.
"""

from .resonance_synthesizer import ResonanceSynthesizer

__all__ = [
    "ResonanceSynthesizer"
]