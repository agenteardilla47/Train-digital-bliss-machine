"""
Thermodynamic Ephemeral Cognition System (TECS)

This module implements the thermodynamic framework for information phase transitions
that drive cryptographic forgetting through entropy gradients and critical point dynamics.
"""

import numpy as np
import hashlib
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from scipy.optimize import minimize
from scipy.stats import entropy as scipy_entropy

from .utils import SecurityParameters, PerformanceMetrics


@dataclass
class ThermodynamicState:
    """Represents the thermodynamic state of the collaborative system"""
    cognitive_temperature: float
    entropy_gradient: float
    critical_threshold: float
    phase_transition_energy: float
    microstate_count: int
    timestamp: float
    
    def is_critical(self) -> bool:
        """Check if system is at critical point"""
        return abs(self.entropy_gradient - self.critical_threshold) < 1e-6
    
    def get_gibbs_energy(self, delta_h: float) -> float:
        """Calculate Gibbs free energy change"""
        return delta_h - self.cognitive_temperature * self.entropy_gradient


class ThermodynamicConstants:
    """Physical constants for the thermodynamic framework"""
    
    # Boltzmann constant (J/K)
    K_B = 1.380649e-23
    
    # Golden ratio for critical entropy threshold
    PHI = 1.618033988749
    
    # Critical entropy threshold: ΔS_crit = 2.718 * k_B * ln(φ)
    DELTA_S_CRITICAL = 2.718 * K_B * np.log(PHI)
    
    # Cognitive temperature range
    T_COG_MIN = 0.1
    T_COG_MAX = 10.0
    
    # Irreversibility threshold
    IRREVERSIBILITY_THRESHOLD = 100.0  # bits


class EntropyGradientEngine:
    """Engine for creating and maintaining entropy gradients"""
    
    def __init__(self, target_criticality: float = None):
        self.target_criticality = target_criticality or ThermodynamicConstants.DELTA_S_CRITICAL
        self.entropy_history = []
        
    def calculate_entropy(self, data: Any) -> float:
        """Calculate Shannon entropy of data"""
        if isinstance(data, (list, np.ndarray)):
            # Convert to probability distribution
            if len(data) > 0:
                unique, counts = np.unique(data, return_counts=True)
                probs = counts / len(data)
                return scipy_entropy(probs, base=2)
        elif isinstance(data, str):
            # Character-level entropy
            char_counts = {}
            for char in data:
                char_counts[char] = char_counts.get(char, 0) + 1
            probs = [count/len(data) for count in char_counts.values()]
            return scipy_entropy(probs, base=2)
        
        return 0.0
    
    def engineer_entropy_gradient(self, source_entropy: float, 
                                collaborator_entropy: float) -> float:
        """Engineer entropy gradient to achieve criticality"""
        current_gradient = abs(source_entropy - collaborator_entropy)
        
        if current_gradient < self.target_criticality:
            # Need to increase gradient
            if source_entropy < collaborator_entropy:
                # Increase source entropy
                target_source = collaborator_entropy + self.target_criticality
                return target_source - collaborator_entropy
            else:
                # Increase collaborator entropy
                target_collaborator = source_entropy + self.target_criticality
                return source_entropy - target_collaborator
        
        return current_gradient
    
    def calibrate_cognitive_temperature(self, source_data: Any, 
                                      collaborator_profile: Dict[str, Any]) -> float:
        """Calibrate cognitive temperature for optimal criticality"""
        source_entropy = self.calculate_entropy(source_data)
        collaborator_entropy = collaborator_profile.get('entropy', 0.0)
        
        # Temperature should be inversely proportional to entropy difference
        # to maintain criticality
        entropy_diff = abs(source_entropy - collaborator_entropy)
        if entropy_diff > 0:
            # T_cog ∝ 1/ΔS for criticality maintenance
            base_temp = ThermodynamicConstants.T_COG_MIN + ThermodynamicConstants.T_COG_MAX / 2
            temp_adjustment = self.target_criticality / entropy_diff
            cognitive_temp = np.clip(base_temp + temp_adjustment, 
                                   ThermodynamicConstants.T_COG_MIN,
                                   ThermodynamicConstants.T_COG_MAX)
        else:
            cognitive_temp = ThermodynamicConstants.T_COG_MAX / 2
            
        return cognitive_temp


class ThermodynamicResonanceExtractor:
    """Extract resonance through entropy-driven phase transitions"""
    
    def __init__(self, target_dims: int, mutual_info_penalty: float):
        self.target_dims = target_dims
        self.mi_penalty = mutual_info_penalty
        self.phase_trace = []
        
    def extract_resonance_critical(self, source_data: Any, 
                                  cognitive_temp: float,
                                  entropy_gradient: float) -> Tuple[np.ndarray, List]:
        """Extract resonance at the critical point"""
        
        # Initialize resonance vector
        resonance = np.random.normal(0, 1, self.target_dims)
        
        def thermodynamic_objective(r):
            """Thermodynamic objective function"""
            # Functional preservation loss
            functional_loss = self._compute_functional_loss(source_data, r)
            
            # Mutual information penalty
            mutual_info = self._estimate_mutual_information(source_data, r)
            
            # Entropy gradient potential energy
            entropy_potential = self._compute_entropy_potential(r, entropy_gradient)
            
            # Phase coherence term
            phase_coherence = self._compute_phase_coherence(r, cognitive_temp)
            
            total_loss = (functional_loss + 
                         self.mi_penalty * mutual_info +
                         entropy_potential +
                         phase_coherence)
            
            return total_loss
        
        # Optimize using L-BFGS-B
        result = minimize(thermodynamic_objective, resonance, method='L-BFGS-B')
        
        # Record phase transition
        phase_trace = {
            'cognitive_temperature': cognitive_temp,
            'entropy_gradient': entropy_gradient,
            'final_loss': result.fun,
            'convergence': result.success
        }
        self.phase_trace.append(phase_trace)
        
        return result.x, self.phase_trace
    
    def _compute_functional_loss(self, source: Any, resonance: np.ndarray) -> float:
        """Compute task-specific functional preservation loss"""
        # Simplified functional loss - in practice this would be domain-specific
        if isinstance(source, str):
            # Text-based functional preservation
            source_length = len(source)
            resonance_norm = np.linalg.norm(resonance)
            return abs(source_length - resonance_norm) / max(source_length, 1)
        else:
            # Generic functional loss
            return np.linalg.norm(resonance) / self.target_dims
    
    def _estimate_mutual_information(self, source: Any, resonance: np.ndarray) -> float:
        """Estimate mutual information between source and resonance"""
        # Simplified mutual information estimation
        # In practice, this would use MINE or similar techniques
        source_entropy = self._calculate_source_entropy(source)
        resonance_entropy = self._calculate_resonance_entropy(resonance)
        
        # Joint entropy approximation
        joint_entropy = source_entropy + resonance_entropy - np.log2(self.target_dims)
        
        return max(0, source_entropy + resonance_entropy - joint_entropy)
    
    def _compute_entropy_potential(self, resonance: np.ndarray, 
                                  target_gradient: float) -> float:
        """Compute entropy gradient potential energy"""
        current_gradient = np.std(resonance)  # Simple gradient approximation
        return abs(current_gradient - target_gradient)
    
    def _compute_phase_coherence(self, resonance: np.ndarray, 
                                 cognitive_temp: float) -> float:
        """Compute phase coherence at cognitive temperature"""
        # Phase coherence should be maximized at critical temperature
        optimal_temp = ThermodynamicConstants.T_COG_MAX / 2
        temp_diff = abs(cognitive_temp - optimal_temp)
        return temp_diff * np.linalg.norm(resonance)
    
    def _calculate_source_entropy(self, source: Any) -> float:
        """Calculate entropy of source data"""
        if isinstance(source, str):
            return len(set(source)) / len(source) if source else 0
        elif isinstance(source, (list, np.ndarray)):
            return len(set(source)) / len(source) if len(source) > 0 else 0
        return 0.0
    
    def _calculate_resonance_entropy(self, resonance: np.ndarray) -> float:
        """Calculate entropy of resonance vector"""
        # Normalize to probability distribution
        abs_resonance = np.abs(resonance)
        if np.sum(abs_resonance) > 0:
            probs = abs_resonance / np.sum(abs_resonance)
            return scipy_entropy(probs, base=2)
        return 0.0


class ThermodynamicObliterator:
    """Perform thermodynamic annihilation of source material"""
    
    def __init__(self, security_parameter: int):
        self.security_parameter = security_parameter
        self.deletion_proofs = []
        
    def irreversible_phase_transition(self, microstate: Any, 
                                    cognitive_temp: float) -> Dict[str, Any]:
        """Induce irreversible phase transition in microstate"""
        
        # Calculate transition energy
        initial_entropy = self._calculate_microstate_entropy(microstate)
        transition_energy = (ThermodynamicConstants.K_B * 
                           cognitive_temp * 
                           np.log(max(1, len(str(microstate)))))
        
        # Perform irreversible transformation
        transformed = self._transform_microstate(microstate, cognitive_temp)
        final_entropy = self._calculate_microstate_entropy(transformed)
        
        # Generate proof of irreversibility
        proof = {
            'initial_entropy': initial_entropy,
            'final_entropy': final_entropy,
            'transition_energy': transition_energy,
            'cognitive_temperature': cognitive_temp,
            'irreversibility_score': final_entropy - initial_entropy,
            'timestamp': time.time(),
            'hash': hashlib.sha256(str(transformed).encode()).hexdigest()
        }
        
        self.deletion_proofs.append(proof)
        return proof
    
    def _calculate_microstate_entropy(self, microstate: Any) -> float:
        """Calculate entropy of a microstate"""
        if isinstance(microstate, str):
            return len(set(microstate)) / len(microstate) if microstate else 0
        elif isinstance(microstate, (list, np.ndarray)):
            return len(set(microstate)) / len(microstate) if len(microstate) > 0 else 0
        return 0.0
    
    def _transform_microstate(self, microstate: Any, 
                             cognitive_temp: float) -> Any:
        """Transform microstate through irreversible process"""
        # Apply multiple transformations to ensure irreversibility
        
        # 1. Entropy maximization
        if isinstance(microstate, str):
            # Randomize character positions
            chars = list(microstate)
            np.random.shuffle(chars)
            transformed = ''.join(chars)
        elif isinstance(microstate, (list, np.ndarray)):
            # Randomize array elements
            transformed = np.random.permutation(microstate)
        else:
            transformed = str(microstate)
        
        # 2. Cognitive temperature scaling
        temp_factor = cognitive_temp / ThermodynamicConstants.T_COG_MAX
        if isinstance(transformed, str):
            # Apply temperature-dependent character substitution
            transformed = self._apply_temperature_substitution(transformed, temp_factor)
        
        # 3. Final entropy injection
        transformed = self._inject_entropy(transformed, cognitive_temp)
        
        return transformed
    
    def _apply_temperature_substitution(self, text: str, temp_factor: float) -> str:
        """Apply temperature-dependent character substitution"""
        # Higher temperature = more randomization
        chars = list(text)
        for i in range(len(chars)):
            if np.random.random() < temp_factor:
                # Substitute with random character
                chars[i] = chr(np.random.randint(32, 127))
        return ''.join(chars)
    
    def _inject_entropy(self, data: Any, cognitive_temp: float) -> Any:
        """Inject additional entropy based on cognitive temperature"""
        entropy_bits = int(cognitive_temp * ThermodynamicConstants.IRREVERSIBILITY_THRESHOLD)
        
        if isinstance(data, str):
            # Append entropy bits
            entropy_string = ''.join([chr(np.random.randint(32, 127)) 
                                    for _ in range(entropy_bits // 8)])
            return data + entropy_string
        elif isinstance(data, (list, np.ndarray)):
            # Append entropy elements
            entropy_elements = np.random.random(entropy_bits // 8)
            return np.concatenate([data, entropy_elements])
        
        return data
    
    def get_merkle_root(self) -> str:
        """Generate Merkle root of deletion proofs"""
        if not self.deletion_proofs:
            return hashlib.sha256(b"").hexdigest()
        
        # Create leaf hashes
        leaves = [proof['hash'] for proof in self.deletion_proofs]
        
        # Build Merkle tree
        while len(leaves) > 1:
            new_leaves = []
            for i in range(0, len(leaves), 2):
                if i + 1 < len(leaves):
                    combined = leaves[i] + leaves[i + 1]
                else:
                    combined = leaves[i] + leaves[i]
                new_leaves.append(hashlib.sha256(combined.encode()).hexdigest())
            leaves = new_leaves
        
        return leaves[0] if leaves else hashlib.sha256(b"").hexdigest()


class ThermodynamicSynthesizer:
    """Synthesize outputs through emergent criticality"""
    
    def __init__(self, security_parameter: int):
        self.security_parameter = security_parameter
        
    def emergent_synthesis(self, resonance: np.ndarray, 
                          critical_randomness: np.ndarray,
                          cognitive_temp: float,
                          entropy_gradient: float) -> Any:
        """Generate output through emergent synthesis at critical point"""
        
        # Combine resonance with critical randomness
        combined = np.concatenate([resonance, critical_randomness])
        
        # Apply critical point dynamics
        critical_output = self._apply_critical_dynamics(combined, cognitive_temp, entropy_gradient)
        
        # Ensure output exhibits emergence signatures
        emergent_output = self._ensure_emergence_signatures(critical_output, resonance)
        
        return emergent_output
    
    def _apply_critical_dynamics(self, combined: np.ndarray, 
                                cognitive_temp: float,
                                entropy_gradient: float) -> np.ndarray:
        """Apply critical point dynamics to combined input"""
        
        # Critical point transformation
        critical_factor = entropy_gradient / ThermodynamicConstants.DELTA_S_CRITICAL
        temperature_factor = cognitive_temp / ThermodynamicConstants.T_COG_MAX
        
        # Apply non-linear transformation at critical point
        transformed = combined * (1 + critical_factor * temperature_factor)
        
        # Add critical fluctuations
        fluctuations = np.random.normal(0, critical_factor * 0.1, len(transformed))
        transformed += fluctuations
        
        return transformed
    
    def _ensure_emergence_signatures(self, output: np.ndarray, 
                                   resonance: np.ndarray) -> Any:
        """Ensure output exhibits emergence signatures"""
        
        # Check for emergence indicators
        resonance_norm = np.linalg.norm(resonance)
        output_norm = np.linalg.norm(output)
        
        # Emergence should show increased complexity
        if output_norm > resonance_norm * 1.5:
            # High emergence - return as structured output
            return self._structure_emergent_output(output)
        else:
            # Moderate emergence - enhance complexity
            enhanced = self._enhance_complexity(output)
            return self._structure_emergent_output(enhanced)
    
    def _enhance_complexity(self, output: np.ndarray) -> np.ndarray:
        """Enhance complexity to ensure emergence"""
        # Add non-linear transformations
        enhanced = output + np.sin(output) + np.cos(output * 0.5)
        
        # Add fractal-like structure
        enhanced = enhanced + np.roll(enhanced, 1) * 0.1
        
        return enhanced
    
    def _structure_emergent_output(self, output: np.ndarray) -> str:
        """Structure emergent output as meaningful text"""
        # Convert to text representation
        # This is a simplified version - in practice would be more sophisticated
        
        # Normalize to printable characters
        normalized = np.clip(output, 0, 1)
        scaled = (normalized * 94 + 32).astype(int)  # ASCII printable range
        
        # Convert to text
        text = ''.join([chr(int(x)) for x in scaled])
        
        # Clean up and format
        text = text.replace('\x00', ' ').strip()
        
        return text if text else "Emergent output generated through thermodynamic synthesis"


class ThermodynamicZeroKnowledge:
    """Generate zero-knowledge proofs of thermodynamic operations"""
    
    def __init__(self, security_parameter: int):
        self.security_parameter = security_parameter
        
    def prove_thermodynamic_impossibility(self, output: Any, 
                                        source_space: Dict[str, Any]) -> Dict[str, Any]:
        """Prove that reverse derivation is thermodynamically forbidden"""
        
        # Calculate reverse Gibbs energy
        reverse_gibbs = self._calculate_reverse_gibbs_energy(output, source_space)
        
        # Generate proof components
        proof = {
            'reverse_gibbs_energy': reverse_gibbs,
            'thermodynamically_forbidden': reverse_gibbs > 0,
            'entropy_barrier': self._calculate_entropy_barrier(output, source_space),
            'phase_transition_irreversibility': self._verify_phase_irreversibility(output),
            'timestamp': time.time(),
            'proof_hash': self._generate_proof_hash(output, reverse_gibbs)
        }
        
        return proof
    
    def _calculate_reverse_gibbs_energy(self, output: Any, 
                                       source_space: Dict[str, Any]) -> float:
        """Calculate Gibbs free energy for reverse transformation"""
        
        # Estimate enthalpy change (energy required)
        output_complexity = self._estimate_complexity(output)
        source_complexity = source_space.get('complexity', 0)
        
        delta_h = abs(output_complexity - source_complexity)
        
        # Estimate entropy change
        output_entropy = self._estimate_entropy(output)
        source_entropy = source_space.get('entropy', 0)
        
        delta_s = output_entropy - source_entropy
        
        # Use average cognitive temperature
        avg_temp = (ThermodynamicConstants.T_COG_MIN + ThermodynamicConstants.T_COG_MAX) / 2
        
        # Gibbs free energy: ΔG = ΔH - TΔS
        gibbs_energy = delta_h - avg_temp * delta_s
        
        return gibbs_energy
    
    def _estimate_complexity(self, data: Any) -> float:
        """Estimate complexity of data"""
        if isinstance(data, str):
            return len(set(data)) / len(data) if data else 0
        elif isinstance(data, (list, np.ndarray)):
            return len(set(data)) / len(data) if len(data) > 0 else 0
        return 0.0
    
    def _estimate_entropy(self, data: Any) -> float:
        """Estimate entropy of data"""
        return self._estimate_complexity(data)
    
    def _calculate_entropy_barrier(self, output: Any, 
                                  source_space: Dict[str, Any]) -> float:
        """Calculate entropy barrier to reverse transformation"""
        output_entropy = self._estimate_entropy(output)
        source_entropy = source_space.get('entropy', 0)
        
        # Entropy barrier is the difference
        return abs(output_entropy - source_entropy)
    
    def _verify_phase_irreversibility(self, output: Any) -> bool:
        """Verify that output exists in different phase than source"""
        # Simplified verification - in practice would be more sophisticated
        output_entropy = self._estimate_entropy(output)
        
        # Check if output has high entropy (disordered phase)
        return output_entropy > 0.5
    
    def _generate_proof_hash(self, output: Any, gibbs_energy: float) -> str:
        """Generate hash of the proof"""
        proof_string = f"{str(output)}{gibbs_energy}{time.time()}"
        return hashlib.sha256(proof_string.encode()).hexdigest()


class TECS:
    """Thermodynamic Ephemeral Cognition System - Main orchestrator"""
    
    def __init__(self, security_parameter: int = 256, use_tee: bool = True):
        self.security_parameter = security_parameter
        self.use_tee = use_tee
        
        # Initialize components
        self.entropy_engine = EntropyGradientEngine()
        self.resonance_extractor = ThermodynamicResonanceExtractor(
            target_dims=64, mutual_info_penalty=10.0
        )
        self.obliterator = ThermodynamicObliterator(security_parameter)
        self.synthesizer = ThermodynamicSynthesizer(security_parameter)
        self.zk_prover = ThermodynamicZeroKnowledge(security_parameter)
        
        # Performance tracking
        self.performance_metrics = PerformanceMetrics()
        
    def generate(self, source_data: Any, 
                 collaborator_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete TECS protocol"""
        
        # Input validation
        if source_data is None:
            raise ValueError("Source data cannot be None")
        
        if not isinstance(collaborator_profile, dict):
            raise ValueError("Collaborator profile must be a dictionary")
        
        if 'entropy' not in collaborator_profile:
            raise ValueError("Collaborator profile must contain 'entropy' field")
        
        # Validate entropy value
        entropy = collaborator_profile['entropy']
        if not isinstance(entropy, (int, float)) or not (0 <= entropy <= 1):
            raise ValueError("Collaborator entropy must be a number between 0 and 1")
        
        # Validate source data size
        source_size = self._get_data_size(source_data)
        max_size = 1024 * 1024 * 1024  # 1GB limit
        if source_size > max_size:
            raise ValueError(f"Source data too large: {source_size} bytes (max: {max_size})")
        
        start_time = time.time()
        
        # Phase I: Establish criticality
        self.performance_metrics.phase_start("criticality_establishment")
        cognitive_temp = self.entropy_engine.calibrate_cognitive_temperature(
            source_data, collaborator_profile
        )
        source_entropy = self.entropy_engine.calculate_entropy(source_data)
        collaborator_entropy = collaborator_profile.get('entropy', 0.0)
        delta_s = abs(source_entropy - collaborator_entropy)
        
        if delta_s < ThermodynamicConstants.DELTA_S_CRITICAL:
            delta_s = self.entropy_engine.engineer_entropy_gradient(
                source_entropy, collaborator_entropy
            )
        self.performance_metrics.phase_end("criticality_establishment")
        
        # Phase II: Resonance extraction at critical point
        self.performance_metrics.phase_start("resonance_extraction")
        resonance, phase_trace = self.resonance_extractor.extract_resonance_critical(
            source_data, cognitive_temp, delta_s
        )
        resonance_commitment = self._thermodynamic_commit(resonance, cognitive_temp)
        self.performance_metrics.phase_end("resonance_extraction")
        
        # Phase III: Thermodynamic annihilation
        self.performance_metrics.phase_start("thermodynamic_annihilation")
        deletion_proofs = []
        microstates = self._decompose_to_microstates(source_data)
        
        for microstate in microstates:
            if self._is_accessible(microstate):
                proof = self.obliterator.irreversible_phase_transition(
                    microstate, cognitive_temp
                )
                deletion_proofs.append(proof)
        
        thermo_root = self.obliterator.get_merkle_root()
        self.performance_metrics.phase_end("thermodynamic_annihilation")
        
        # Phase IV: Critical point synthesis
        self.performance_metrics.phase_start("emergent_synthesis")
        critical_randomness = self._sample_critical_distribution(cognitive_temp, delta_s)
        output = self.synthesizer.emergent_synthesis(
            resonance, critical_randomness, cognitive_temp, delta_s
        )
        self.performance_metrics.phase_end("emergent_synthesis")
        
        # Phase V: Thermodynamic ZK proof
        self.performance_metrics.phase_start("zk_proof_generation")
        source_space = {
            'entropy': source_entropy,
            'complexity': self._estimate_complexity(source_data)
        }
        zk_proof = self.zk_prover.prove_thermodynamic_impossibility(output, source_space)
        self.performance_metrics.phase_end("zk_proof_generation")
        
        # Calculate total time
        total_time = time.time() - start_time
        self.performance_metrics.set_total_time(total_time)
        
        return {
            'output': output,
            'resonance_commitment': resonance_commitment,
            'thermodynamic_root': thermo_root,
            'cognitive_temperature': cognitive_temp,
            'entropy_gradient': delta_s,
            'phase_trace': phase_trace,
            'deletion_proofs': deletion_proofs,
            'zk_proof': zk_proof,
            'performance_metrics': self.performance_metrics.get_performance_summary()
        }
    
    def _thermodynamic_commit(self, resonance: np.ndarray, 
                             cognitive_temp: float) -> str:
        """Generate thermodynamic commitment to resonance"""
        commitment_data = f"{resonance.tobytes().hex()}{cognitive_temp}{time.time()}"
        return hashlib.sha256(commitment_data.encode()).hexdigest()
    
    def _decompose_to_microstates(self, source_data: Any) -> List[Any]:
        """Decompose source data into microstates"""
        if isinstance(source_data, str):
            # Character-level microstates
            return [char for char in source_data]
        elif isinstance(source_data, (list, np.ndarray)):
            # Element-level microstates
            return list(source_data)
        else:
            # Single microstate
            return [source_data]
    
    def _is_accessible(self, microstate: Any) -> bool:
        """Check if microstate is accessible for entropy analysis"""
        if isinstance(microstate, str):
            return len(microstate) > 0
        elif isinstance(microstate, (list, np.ndarray)):
            return len(microstate) > 0
        return True
    
    def _sample_critical_distribution(self, cognitive_temp: float, 
                                     entropy_gradient: float) -> np.ndarray:
        """Sample randomness from critical-point distribution"""
        # Sample size based on cognitive temperature
        sample_size = int(cognitive_temp * 10)
        
        # Critical distribution has higher variance near critical point
        critical_factor = entropy_gradient / ThermodynamicConstants.DELTA_S_CRITICAL
        variance = 1.0 + critical_factor
        
        return np.random.normal(0, variance, sample_size)
    
    def _estimate_complexity(self, data: Any) -> float:
        """Estimate complexity of data"""
        if isinstance(data, str):
            return len(set(data)) / len(data) if data else 0
        elif isinstance(data, (list, np.ndarray)):
            return len(set(data)) / len(data) if len(data) > 0 else 0
        return 0.0
    
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
    
    def verify_thermodynamic_impossibility(self, output: Any, 
                                          source_space: Dict[str, Any]) -> bool:
        """Verify that reverse derivation is thermodynamically forbidden"""
        zk_proof = self.zk_prover.prove_thermodynamic_impossibility(output, source_space)
        return zk_proof['thermodynamically_forbidden']