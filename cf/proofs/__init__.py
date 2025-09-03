"""
Zero-Knowledge Deletion Proofs

This module implements Phase 4 of the CF protocol: generating zero-knowledge
proofs that attest to correct execution of the forgetting protocol.
"""

from .deletion_proof_generator import DeletionProofGenerator

__all__ = [
    "DeletionProofGenerator"
]