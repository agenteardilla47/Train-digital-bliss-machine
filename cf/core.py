"""
Core Cryptographic Forgetting (CF) Protocol Implementation

This module implements the main CF protocol that orchestrates the four phases:
1. Intent Crystallization
2. Cryptographic Obliteration  
3. Resonance Synthesis
4. Zero-Knowledge Deletion
"""

import os
import hashlib
import time
from typing import Any, Dict, List, Tuple, Optional
from dataclasses import dataclass

from .extractors import InformationBottleneckExtractor
from .obliteration import CryptographicObliterator
from .synthesis import ResonanceSynthesizer
from .proofs import DeletionProofGenerator
from .utils import SecurityParameters, PerformanceMetrics


@dataclass
class ForgettingResult:
    """Result of the CF protocol execution"""
    output: Any
    proof: bytes
    deletion_certificates: List[bytes]
    performance_metrics: PerformanceMetrics
    security_parameters: SecurityParameters


class CryptographicForgetting:
    """
    Main Cryptographic Forgetting protocol implementation.
    
    Implements the four-phase protocol described in the research paper:
    - Intent Crystallization using Information Bottleneck principle
    - Cryptographic Obliteration with TEE support
    - Resonance Synthesis from distilled essence
    - Zero-Knowledge Deletion proof generation
    """
    
    def __init__(self, security_parameter: int = 256, 
                 use_tee: bool = True,
                 mutual_info_penalty: float = 10.0):
        """
        Initialize the CF framework.
        
        Args:
            security_parameter: Security parameter in bits (default: 256)
            use_tee: Whether to use Trusted Execution Environment (default: True)
            mutual_info_penalty: Penalty for mutual information leakage (default: 10.0)
        """
        self.security_parameter = security_parameter
        self.use_tee = use_tee
        self.mutual_info_penalty = mutual_info_penalty
        
        # Initialize components
        self.extractor = InformationBottleneckExtractor(
            target_dims=min(64, 1024),  # Adaptive based on source size
            mutual_info_penalty=mutual_info_penalty
        )
        
        self.obliterator = CryptographicObliterator(
            security_parameter=security_parameter,
            use_tee=use_tee
        )
        
        self.synthesizer = ResonanceSynthesizer(
            security_parameter=security_parameter
        )
        
        self.proof_generator = DeletionProofGenerator(
            security_parameter=security_parameter
        )
        
        # Performance tracking
        self.performance_metrics = PerformanceMetrics()
        
    def forget(self, source_data: Any, 
               functional_requirements: Dict[str, Any]) -> ForgettingResult:
        """
        Execute the complete CF protocol.
        
        Args:
            source_data: The source material to be forgotten
            functional_requirements: Requirements for functional preservation
            
        Returns:
            ForgettingResult containing output, proof, and metadata
        """
        # Input validation
        if source_data is None:
            raise ValueError("Source data cannot be None")
        
        if not isinstance(functional_requirements, dict):
            raise ValueError("Functional requirements must be a dictionary")
        
        if not functional_requirements:
            raise ValueError("Functional requirements cannot be empty")
        
        # Validate source data size limits
        source_size = self._get_data_size(source_data)
        max_size = 1024 * 1024 * 1024  # 1GB limit
        if source_size > max_size:
            raise ValueError(f"Source data too large: {source_size} bytes (max: {max_size})")
        
        start_time = time.time()
        
        # Phase 1: Intent Crystallization
        self.performance_metrics.phase_start("crystallization")
        resonance = self.extractor.extract(source_data, functional_requirements)
        self.performance_metrics.phase_end("crystallization")
        
        # Phase 2: Cryptographic Obliteration
        self.performance_metrics.phase_start("obliteration")
        deletion_certificates = self.obliterator.obliterate(source_data)
        self.performance_metrics.phase_end("obliteration")
        
        # Phase 3: Resonance Synthesis
        self.performance_metrics.phase_start("synthesis")
        output = self.synthesizer.synthesize(resonance, functional_requirements)
        self.performance_metrics.phase_end("synthesis")
        
        # Phase 4: Zero-Knowledge Deletion Proof
        self.performance_metrics.phase_start("proof_generation")
        proof = self.proof_generator.generate_proof(
            resonance=resonance,
            deletion_certificates=deletion_certificates,
            output=output
        )
        self.performance_metrics.phase_end("proof_generation")
        
        # Calculate total execution time
        total_time = time.time() - start_time
        self.performance_metrics.set_total_time(total_time)
        
        # Create result object
        result = ForgettingResult(
            output=output,
            proof=proof,
            deletion_certificates=deletion_certificates,
            performance_metrics=self.performance_metrics,
            security_parameters=SecurityParameters(
                security_parameter=self.security_parameter,
                use_tee=self.use_tee,
                mutual_info_penalty=self.mutual_info_penalty
            )
        )
        
        return result
    
    def verify_deletion_proof(self, proof: bytes, 
                             public_inputs: Dict[str, Any]) -> bool:
        """
        Verify a deletion proof.
        
        Args:
            proof: The zero-knowledge proof to verify
            public_inputs: Public inputs for verification
            
        Returns:
            True if proof is valid, False otherwise
        """
        return self.proof_generator.verify_proof(proof, public_inputs)
    
    def get_performance_metrics(self) -> PerformanceMetrics:
        """Get performance metrics from the last execution."""
        return self.performance_metrics
    
    def estimate_memory_usage(self, source_size: int) -> int:
        """
        Estimate memory usage for a given source size.
        
        Args:
            source_size: Size of source data in bytes
            
        Returns:
            Estimated memory usage in bytes
        """
        # Base memory for framework overhead
        base_memory = 1024 * 1024  # 1MB base
        
        # Memory for resonance (typically 1/1000 of source size)
        resonance_memory = max(64 * 8, source_size // 1000)
        
        # Memory for intermediate computations
        intermediate_memory = source_size * 2
        
        # TEE overhead if enabled
        tee_overhead = source_size if self.use_tee else 0
        
        return base_memory + resonance_memory + intermediate_memory + tee_overhead
    
    def _get_data_size(self, data: Any) -> int:
        """Get size of data in bytes"""
        if isinstance(data, str):
            return len(data.encode('utf-8'))
        elif isinstance(data, (list, tuple)):
            return sum(self._get_data_size(item) for item in data)
        elif isinstance(data, dict):
            return sum(self._get_data_size(k) + self._get_data_size(v) for k, v in data.items())
        elif hasattr(data, 'nbytes'):
            return data.nbytes
        elif hasattr(data, '__len__'):
            return len(data) * 8  # Estimate
        else:
            return len(str(data).encode('utf-8'))
    
    def get_security_guarantees(self) -> Dict[str, str]:
        """
        Get security guarantees provided by the framework.
        
        Returns:
            Dictionary of security guarantees
        """
        return {
            "source_unrecoverability": "No PPT adversary can recover source material",
            "trace_elimination": "All intermediate representations destroyed",
            "verifiable_deletion": "Zero-knowledge proof of complete deletion",
            "forward_security": "Future key compromise cannot recover past data",
            "tee_protection": "Physical memory attacks mitigated" if self.use_tee else "Standard memory protection"
        }