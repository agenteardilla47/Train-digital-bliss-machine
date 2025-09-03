"""
Utility classes and functions for the CF framework.

This module provides:
- SecurityParameters: Configuration for security settings
- PerformanceMetrics: Tracking of execution performance
- Security utilities and constants
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class SecurityLevel(Enum):
    """Security levels for the CF framework"""
    STANDARD = 128
    HIGH = 256
    ULTRA = 512


@dataclass
class SecurityParameters:
    """Security configuration parameters"""
    security_parameter: int = 256
    use_tee: bool = True
    mutual_info_penalty: float = 10.0
    deletion_passes: int = 7  # Gutmann's algorithm
    entropy_bits: int = 256
    proof_system: str = "Groth16"
    
    def __post_init__(self):
        """Validate security parameters"""
        if self.security_parameter not in [128, 256, 512]:
            raise ValueError("Security parameter must be 128, 256, or 512")
        if self.mutual_info_penalty <= 0:
            raise ValueError("Mutual information penalty must be positive")
        if self.deletion_passes < 3:
            raise ValueError("Deletion passes must be at least 3")
    
    def get_security_level(self) -> SecurityLevel:
        """Get the security level enum value"""
        if self.security_parameter == 128:
            return SecurityLevel.STANDARD
        elif self.security_parameter == 256:
            return SecurityLevel.HIGH
        else:
            return SecurityLevel.ULTRA
    
    def get_attack_complexity(self) -> str:
        """Get the computational complexity for attacks"""
        if self.security_parameter == 128:
            return "2^128 operations"
        elif self.security_parameter == 256:
            return "2^256 operations"
        else:
            return "2^512 operations"


@dataclass
class PerformanceMetrics:
    """Performance tracking for CF protocol phases"""
    phase_times: Dict[str, float] = field(default_factory=dict)
    phase_memory: Dict[str, int] = field(default_factory=dict)
    total_time: float = 0.0
    total_memory: int = 0
    start_time: Optional[float] = None
    
    def phase_start(self, phase_name: str):
        """Start timing a phase"""
        self.start_time = time.time()
    
    def phase_end(self, phase_name: str, memory_usage: int = 0):
        """End timing a phase and record metrics"""
        if self.start_time is not None:
            duration = time.time() - self.start_time
            self.phase_times[phase_name] = duration
            self.phase_memory[phase_name] = memory_usage
            self.total_memory += memory_usage
            self.start_time = None
    
    def set_total_time(self, total_time: float):
        """Set the total execution time"""
        self.total_time = total_time
    
    def get_phase_time(self, phase_name: str) -> float:
        """Get execution time for a specific phase"""
        return self.phase_times.get(phase_name, 0.0)
    
    def get_phase_memory(self, phase_name: str) -> int:
        """Get memory usage for a specific phase"""
        return self.phase_memory.get(phase_name, 0)
    
    def get_total_phase_time(self) -> float:
        """Get total time across all phases"""
        return sum(self.phase_times.values())
    
    def get_overhead_time(self) -> float:
        """Get overhead time (total - phase times)"""
        return max(0, self.total_time - self.get_total_phase_time())
    
    def get_performance_summary(self) -> Dict[str, any]:
        """Get a summary of all performance metrics"""
        return {
            "total_time": self.total_time,
            "total_memory": self.total_memory,
            "phase_times": self.phase_times,
            "phase_memory": self.phase_memory,
            "overhead_time": self.get_overhead_time(),
            "efficiency": self.get_total_phase_time() / max(self.total_time, 1e-9)
        }


# Security constants
SECURITY_CONSTANTS = {
    "MIN_ENTROPY_BITS": 128,
    "MAX_ENTROPY_BITS": 512,
    "DEFAULT_DELETION_PASSES": 7,
    "TEE_MEMORY_ALIGNMENT": 4096,
    "RESONANCE_COMPRESSION_RATIO": 1000,  # 1:1000 compression
    "MUTUAL_INFO_THRESHOLD": 1e-6,  # Threshold for correlation detection
}

# Performance benchmarks (from research paper)
PERFORMANCE_BENCHMARKS = {
    "1KB": {"crystallization": 0.1, "obliteration": 0.5, "synthesis": 0.2, "total": 0.8},
    "1MB": {"crystallization": 12.0, "obliteration": 45.0, "synthesis": 8.0, "total": 65.0},
    "100MB": {"crystallization": 1200.0, "obliteration": 4100.0, "synthesis": 900.0, "total": 6200.0},
    "1GB": {"crystallization": 11800.0, "obliteration": 39200.0, "synthesis": 8700.0, "total": 59700.0}
}


def validate_security_parameters(params: SecurityParameters) -> bool:
    """
    Validate security parameters for consistency.
    
    Args:
        params: Security parameters to validate
        
    Returns:
        True if parameters are valid, False otherwise
    """
    try:
        # Check security parameter is valid
        if params.security_parameter not in [128, 256, 512]:
            return False
        
        # Check mutual info penalty is reasonable
        if params.mutual_info_penalty < 0.1 or params.mutual_info_penalty > 100:
            return False
        
        # Check deletion passes
        if params.deletion_passes < 3 or params.deletion_passes > 35:
            return False
        
        # Check entropy bits
        if params.entropy_bits < SECURITY_CONSTANTS["MIN_ENTROPY_BITS"]:
            return False
        
        return True
    except:
        return False


def estimate_performance(source_size: int, security_level: SecurityLevel) -> Dict[str, float]:
    """
    Estimate performance based on source size and security level.
    
    Args:
        source_size: Size of source data in bytes
        security_level: Security level to use
        
    Returns:
        Dictionary with estimated performance metrics
    """
    # Find closest benchmark
    if source_size <= 1024:
        benchmark = PERFORMANCE_BENCHMARKS["1KB"]
    elif source_size <= 1024 * 1024:
        benchmark = PERFORMANCE_BENCHMARKS["1MB"]
    elif source_size <= 100 * 1024 * 1024:
        benchmark = PERFORMANCE_BENCHMARKS["100MB"]
    else:
        benchmark = PERFORMANCE_BENCHMARKS["1GB"]
    
    # Scale by security level
    security_multiplier = {
        SecurityLevel.STANDARD: 1.0,
        SecurityLevel.HIGH: 1.5,
        SecurityLevel.ULTRA: 2.5
    }[security_level]
    
    scaled_benchmark = {}
    for phase, time_ms in benchmark.items():
        if phase != "total":
            scaled_benchmark[phase] = time_ms * security_multiplier / 1000.0  # Convert to seconds
    
    scaled_benchmark["total"] = sum(v for k, v in scaled_benchmark.items() if k != "total")
    
    return scaled_benchmark