"""
Information Bottleneck Extractors for Intent Crystallization

This module implements Phase 1 of the CF protocol: extracting minimal
functional representations while minimizing mutual information with source.
"""

from .information_bottleneck import InformationBottleneckExtractor
from .mine_estimator import MINEEstimator

__all__ = [
    "InformationBottleneckExtractor",
    "MINEEstimator"
]