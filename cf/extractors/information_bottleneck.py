"""
Information Bottleneck Extractor for Intent Crystallization

This module implements Phase 1 of the CF protocol: extracting minimal
functional representations while minimizing mutual information with source.
"""

import numpy as np
import torch
import torch.nn as nn
from typing import Any, Dict, Tuple, Optional
from scipy.optimize import minimize

from .mine_estimator import MINEEstimator


class InformationBottleneckExtractor:
    """
    Extracts minimal functional representations using Information Bottleneck principle.
    
    Implements the objective:
    R = arg min[L_functional(S, r) + λ · I(r; S)]
    where λ controls the mutual information penalty.
    """
    
    def __init__(self, target_dims: int, mutual_info_penalty: float = 10.0):
        """
        Initialize the Information Bottleneck extractor.
        
        Args:
            target_dims: Target dimensionality of resonance vector
            mutual_info_penalty: Penalty coefficient for mutual information
        """
        self.target_dims = target_dims
        self.mi_penalty = mutual_info_penalty
        self.mine_estimator = MINEEstimator()
        self.extraction_history = []
        
    def extract(self, source_data: Any, 
                functional_requirements: Dict[str, Any]) -> np.ndarray:
        """
        Extract resonance using Information Bottleneck principle.
        
        Args:
            source_data: The source material to extract from
            functional_requirements: Requirements for functional preservation
            
        Returns:
            Resonance vector that preserves function while minimizing mutual information
        """
        # Initialize resonance vector
        resonance = np.random.normal(0, 1, self.target_dims)
        
        # Define objective function
        def objective(r):
            functional_loss = self._compute_functional_loss(source_data, r, functional_requirements)
            mutual_info = self._estimate_mutual_information(source_data, r)
            
            total_loss = functional_loss + self.mi_penalty * mutual_info
            return total_loss
        
        # Optimize using L-BFGS-B
        result = minimize(objective, resonance, method='L-BFGS-B')
        
        # Record extraction details
        extraction_record = {
            'source_size': self._get_data_size(source_data),
            'target_dims': self.target_dims,
            'mutual_info_penalty': self.mi_penalty,
            'final_loss': result.fun,
            'convergence': result.success,
            'iterations': result.nit,
            'functional_loss': self._compute_functional_loss(source_data, result.x, functional_requirements),
            'final_mutual_info': self._estimate_mutual_information(source_data, result.x)
        }
        self.extraction_history.append(extraction_record)
        
        return result.x
    
    def _compute_functional_loss(self, source: Any, resonance: np.ndarray, 
                                requirements: Dict[str, Any]) -> float:
        """
        Compute task-specific functional preservation loss.
        
        Args:
            source: Source data
            resonance: Resonance vector
            requirements: Functional requirements
            
        Returns:
            Functional loss value
        """
        loss = 0.0
        
        # Task-specific functional preservation
        if 'task_type' in requirements:
            if requirements['task_type'] == 'text_generation':
                loss += self._text_functional_loss(source, resonance, requirements)
            elif requirements['task_type'] == 'classification':
                loss += self._classification_functional_loss(source, resonance, requirements)
            elif requirements['task_type'] == 'translation':
                loss += self._translation_functional_loss(source, resonance, requirements)
            else:
                # Generic functional loss
                loss += self._generic_functional_loss(source, resonance, requirements)
        else:
            # Default to generic loss
            loss += self._generic_functional_loss(source, resonance, requirements)
        
        # Add regularization terms
        if 'regularization' in requirements:
            if requirements['regularization'] == 'l2':
                loss += 0.01 * np.linalg.norm(resonance) ** 2
            elif requirements['regularization'] == 'l1':
                loss += 0.01 * np.linalg.norm(resonance, ord=1)
        
        return loss
    
    def _compute_semantic_structure_loss(self, source: str, resonance: np.ndarray) -> float:
        """Compute semantic structure loss for text"""
        # Simplified semantic structure loss
        if len(source) == 0:
            return 0.0
        
        # Basic semantic features
        word_count = len(source.split())
        char_diversity = len(set(source)) / len(source)
        
        # Map to resonance space
        resonance_norm = np.linalg.norm(resonance)
        
        # Calculate loss based on structure preservation
        structure_loss = abs(word_count - resonance_norm * 10) / max(word_count, 1)
        diversity_loss = abs(char_diversity - np.std(resonance)) / max(char_diversity, 0.1)
        
        return structure_loss + 0.1 * diversity_loss
    
    def _text_functional_loss(self, source: Any, resonance: np.ndarray, 
                             requirements: Dict[str, Any]) -> float:
        """Compute functional loss for text generation tasks"""
        if isinstance(source, str):
            # Preserve semantic coherence
            source_length = len(source)
            resonance_norm = np.linalg.norm(resonance)
            
            # Length preservation
            length_loss = abs(source_length - resonance_norm) / max(source_length, 1)
            
            # Semantic structure preservation
            semantic_loss = self._compute_semantic_structure_loss(source, resonance)
            
            return length_loss + 0.1 * semantic_loss
        
        return 0.0
    
    def _classification_functional_loss(self, source: Any, resonance: np.ndarray, 
                                      requirements: Dict[str, Any]) -> float:
        """Compute functional loss for classification tasks"""
        if 'target_class' in requirements:
            target_class = requirements['target_class']
            
            # Preserve class-relevant features
            class_features = self._extract_class_features(source, target_class)
            resonance_features = self._extract_resonance_features(resonance)
            
            # Feature alignment loss
            feature_loss = np.linalg.norm(class_features - resonance_features[:len(class_features)])
            
            return feature_loss
        
        return 0.0
    
    def _translation_functional_loss(self, source: Any, resonance: np.ndarray, 
                                    requirements: Dict[str, Any]) -> float:
        """Compute functional loss for translation tasks"""
        if 'source_language' in requirements and 'target_language' in requirements:
            # Preserve cross-lingual semantic mapping
            source_semantics = self._extract_semantic_features(source, requirements['source_language'])
            resonance_semantics = self._extract_resonance_semantics(resonance)
            
            # Semantic mapping preservation
            mapping_loss = np.linalg.norm(source_semantics - resonance_semantics)
            
            return mapping_loss
        
        return 0.0
    
    def _generic_functional_loss(self, source: Any, resonance: np.ndarray, 
                                requirements: Dict[str, Any]) -> float:
        """Compute generic functional loss"""
        # Basic structure preservation
        source_structure = self._extract_structure_features(source)
        resonance_structure = self._extract_resonance_structure(resonance)
        
        # Structure alignment loss
        structure_loss = np.linalg.norm(source_structure - resonance_structure)
        
        # Complexity preservation
        source_complexity = self._estimate_complexity(source)
        resonance_complexity = self._estimate_resonance_complexity(resonance)
        complexity_loss = abs(source_complexity - resonance_complexity)
        
        return structure_loss + 0.1 * complexity_loss
    
    def _estimate_mutual_information(self, source: Any, resonance: np.ndarray) -> float:
        """
        Estimate mutual information between source and resonance.
        
        Args:
            source: Source data
            resonance: Resonance vector
            
        Returns:
            Estimated mutual information
        """
        try:
            # Use MINE estimator if available
            return self.mine_estimator.estimate_mi(source, resonance)
        except:
            # Fallback to simplified estimation
            return self._simplified_mi_estimation(source, resonance)
    
    def _simplified_mi_estimation(self, source: Any, resonance: np.ndarray) -> float:
        """Simplified mutual information estimation"""
        # Calculate entropies
        source_entropy = self._calculate_source_entropy(source)
        resonance_entropy = self._calculate_resonance_entropy(resonance)
        
        # Joint entropy approximation
        joint_entropy = source_entropy + resonance_entropy - np.log2(self.target_dims)
        
        # Mutual information: I(X;Y) = H(X) + H(Y) - H(X,Y)
        mutual_info = max(0, source_entropy + resonance_entropy - joint_entropy)
        
        return mutual_info
    
    def _calculate_source_entropy(self, source: Any) -> float:
        """Calculate entropy of source data"""
        if isinstance(source, str):
            if len(source) == 0:
                return 0.0
            # Character-level entropy
            char_counts = {}
            for char in source:
                char_counts[char] = char_counts.get(char, 0) + 1
            
            probs = [count/len(source) for count in char_counts.values()]
            return self._shannon_entropy(probs)
            
        elif isinstance(source, (list, np.ndarray)):
            if len(source) == 0:
                return 0.0
            # Element-level entropy
            unique, counts = np.unique(source, return_counts=True)
            probs = counts / len(source)
            return self._shannon_entropy(probs)
        
        return 0.0
    
    def _calculate_resonance_entropy(self, resonance: np.ndarray) -> float:
        """Calculate entropy of resonance vector"""
        # Normalize to probability distribution
        abs_resonance = np.abs(resonance)
        if np.sum(abs_resonance) > 0:
            probs = abs_resonance / np.sum(abs_resonance)
            return self._shannon_entropy(probs)
        return 0.0
    
    def _shannon_entropy(self, probs: np.ndarray) -> float:
        """Calculate Shannon entropy from probability distribution"""
        # Remove zero probabilities
        probs = probs[probs > 0]
        if len(probs) == 0:
            return 0.0
        
        # Shannon entropy: H = -Σ p_i * log2(p_i)
        return -np.sum(probs * np.log2(probs))
    
    def _extract_semantic_features(self, source: Any, language: str) -> np.ndarray:
        """Extract semantic features from source"""
        # Simplified semantic feature extraction
        if isinstance(source, str):
            # Basic semantic features based on word frequency
            words = source.lower().split()
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Convert to feature vector
            features = np.zeros(min(100, len(word_freq)))
            for i, (word, freq) in enumerate(list(word_freq.items())[:100]):
                features[i] = freq / len(words)
            
            return features
        
        return np.zeros(100)
    
    def _extract_resonance_semantics(self, resonance: np.ndarray) -> np.ndarray:
        """Extract semantic features from resonance"""
        # Map resonance to semantic space
        semantic_features = resonance[:100]  # Take first 100 dimensions
        if len(semantic_features) < 100:
            semantic_features = np.pad(semantic_features, (0, 100 - len(semantic_features)))
        
        return semantic_features
    
    def _extract_structure_features(self, source: Any) -> np.ndarray:
        """Extract structural features from source"""
        if isinstance(source, str):
            # Structural features: length, character diversity, etc.
            features = np.array([
                len(source),
                len(set(source)) / len(source) if source else 0,
                source.count(' ') / len(source) if source else 0,
                sum(c.isupper() for c in source) / len(source) if source else 0
            ])
            return features
        elif isinstance(source, (list, np.ndarray)):
            # Array structural features
            features = np.array([
                len(source),
                len(set(source)) / len(source) if len(source) > 0 else 0,
                np.std(source) if len(source) > 0 else 0,
                np.mean(source) if len(source) > 0 else 0
            ])
            return features
        
        return np.zeros(4)
    
    def _extract_resonance_structure(self, resonance: np.ndarray) -> np.ndarray:
        """Extract structural features from resonance"""
        features = np.array([
            len(resonance),
            np.std(resonance),
            np.mean(resonance),
            np.linalg.norm(resonance)
        ])
        return features
    
    def _extract_class_features(self, source: Any, target_class: Any) -> np.ndarray:
        """Extract class-relevant features"""
        # Simplified class feature extraction
        if isinstance(source, str):
            # Basic text features
            features = np.array([
                len(source),
                len(set(source)) / len(source) if source else 0,
                hash(target_class) % 1000 / 1000.0  # Class encoding
            ])
            return features
        
        return np.zeros(3)
    
    def _extract_resonance_features(self, resonance: np.ndarray) -> np.ndarray:
        """Extract features from resonance vector"""
        features = np.array([
            np.mean(resonance),
            np.std(resonance),
            np.linalg.norm(resonance)
        ])
        return features
    
    def _estimate_complexity(self, data: Any) -> float:
        """Estimate complexity of data"""
        if isinstance(data, str):
            return len(set(data)) / len(data) if data else 0
        elif isinstance(data, (list, np.ndarray)):
            return len(set(data)) / len(data) if len(data) > 0 else 0
        return 0.0
    
    def _estimate_resonance_complexity(self, resonance: np.ndarray) -> float:
        """Estimate complexity of resonance vector"""
        return np.std(resonance)
    
    def _get_data_size(self, data: Any) -> int:
        """Get size of data in bytes"""
        if isinstance(data, str):
            return len(data.encode('utf-8'))
        elif isinstance(data, (list, np.ndarray)):
            return data.nbytes if hasattr(data, 'nbytes') else len(data) * 8
        return 0
    
    def get_extraction_summary(self) -> Dict[str, Any]:
        """Get summary of extraction performance"""
        if not self.extraction_history:
            return {}
        
        recent = self.extraction_history[-1]
        return {
            'target_dims': self.target_dims,
            'mutual_info_penalty': self.mi_penalty,
            'average_functional_loss': np.mean([r['functional_loss'] for r in self.extraction_history]),
            'average_mutual_info': np.mean([r['final_mutual_info'] for r in self.extraction_history]),
            'convergence_rate': np.mean([r['convergence'] for r in self.extraction_history]),
            'last_extraction': recent
        }