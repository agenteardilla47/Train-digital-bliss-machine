"""
Mutual Information Neural Estimation (MINE) for CF framework

This module implements neural network-based mutual information estimation
as described in the research paper for measuring information leakage.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Any, Tuple, Optional
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')


class MINENetwork(nn.Module):
    """Neural network for mutual information estimation"""
    
    def __init__(self, input_dim: int, hidden_dim: int = 64):
        super(MINENetwork, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
        
        # Initialize weights
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Initialize network weights"""
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the network"""
        return self.network(x)


class MINEEstimator:
    """
    Mutual Information Neural Estimation using MINE algorithm.
    
    Implements the MINE estimator:
    I_MINE(X;Y) = sup_θ E_P(x,y)[T_θ(x,y)] - log(E_P(x)⊗P(y)[e^T_θ(x,y)])
    """
    
    def __init__(self, hidden_dim: int = 64, learning_rate: float = 1e-4,
                 batch_size: int = 256, max_epochs: int = 1000):
        """
        Initialize MINE estimator.
        
        Args:
            hidden_dim: Hidden dimension of neural network
            learning_rate: Learning rate for optimization
            batch_size: Batch size for training
            max_epochs: Maximum training epochs
        """
        self.hidden_dim = hidden_dim
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.max_epochs = max_epochs
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.network = None
        self.optimizer = None
        
        # Training history
        self.training_history = []
        
    def estimate_mi(self, source: Any, resonance: np.ndarray) -> float:
        """
        Estimate mutual information between source and resonance.
        
        Args:
            source: Source data
            resonance: Resonance vector
            
        Returns:
            Estimated mutual information
        """
        try:
            # Convert inputs to tensors
            source_tensor, resonance_tensor = self._prepare_inputs(source, resonance)
            
            # Train the network
            mi_estimate = self._train_and_estimate(source_tensor, resonance_tensor)
            
            return mi_estimate
            
        except Exception as e:
            # Fallback to simplified estimation
            return self._fallback_mi_estimation(source, resonance)
    
    def _prepare_inputs(self, source: Any, resonance: np.ndarray) -> Tuple[torch.Tensor, torch.Tensor]:
        """Prepare inputs for neural network"""
        
        # Convert source to numerical representation
        if isinstance(source, str):
            # Text to numerical features
            source_features = self._text_to_features(source)
        elif isinstance(source, (list, np.ndarray)):
            # Array to features
            source_features = self._array_to_features(source)
        else:
            # Generic object to features
            source_features = self._object_to_features(source)
        
        # Ensure resonance is 2D
        if resonance.ndim == 1:
            resonance = resonance.reshape(-1, 1)
        
        # Pad or truncate to match dimensions
        max_dim = max(source_features.shape[1], resonance.shape[1])
        
        if source_features.shape[1] < max_dim:
            source_features = np.pad(source_features, ((0, 0), (0, max_dim - source_features.shape[1])))
        elif source_features.shape[1] > max_dim:
            source_features = source_features[:, :max_dim]
        
        if resonance.shape[1] < max_dim:
            resonance = np.pad(resonance, ((0, 0), (0, max_dim - resonance.shape[1])))
        elif resonance.shape[1] > max_dim:
            resonance = resonance[:, :max_dim]
        
        # Convert to tensors
        source_tensor = torch.FloatTensor(source_features).to(self.device)
        resonance_tensor = torch.FloatTensor(resonance).to(self.device)
        
        return source_tensor, resonance_tensor
    
    def _text_to_features(self, text: str) -> np.ndarray:
        """Convert text to numerical features"""
        if not text:
            return np.zeros((1, 100))
        
        # Character-level features
        char_features = []
        for char in text[:100]:  # Limit to 100 characters
            char_features.append([
                ord(char),
                char.isupper(),
                char.islower(),
                char.isdigit(),
                char.isspace(),
                hash(char) % 1000 / 1000.0
            ])
        
        # Pad to 100 characters
        while len(char_features) < 100:
            char_features.append([0, 0, 0, 0, 0, 0])
        
        # Convert to 2D array
        features = np.array(char_features)
        
        # Add global text features
        global_features = np.array([
            len(text),
            len(set(text)) / len(text) if text else 0,
            text.count(' ') / len(text) if text else 0,
            sum(c.isupper() for c in text) / len(text) if text else 0,
            sum(c.isdigit() for c in text) / len(text) if text else 0
        ])
        
        # Combine local and global features
        combined = np.concatenate([features, global_features.reshape(1, -1).repeat(100, axis=0)], axis=1)
        
        return combined
    
    def _array_to_features(self, array: Any) -> np.ndarray:
        """Convert array to numerical features"""
        if isinstance(array, list):
            array = np.array(array)
        
        if len(array) == 0:
            return np.zeros((1, 100))
        
        # Statistical features
        features = np.array([
            np.mean(array),
            np.std(array),
            np.min(array),
            np.max(array),
            np.median(array),
            len(array),
            len(set(array)) / len(array) if len(array) > 0 else 0
        ])
        
        # Repeat features to match expected dimensions
        repeated = np.tile(features, (100, 1))
        
        return repeated
    
    def _object_to_features(self, obj: Any) -> np.ndarray:
        """Convert generic object to numerical features"""
        # Hash-based features
        obj_hash = hash(str(obj))
        features = np.array([
            obj_hash % 1000 / 1000.0,
            (obj_hash >> 10) % 1000 / 1000.0,
            (obj_hash >> 20) % 1000 / 1000.0,
            len(str(obj)),
            hash(type(obj).__name__) % 1000 / 1000.0
        ])
        
        # Repeat features
        repeated = np.tile(features, (100, 1))
        
        return repeated
    
    def _train_and_estimate(self, source_tensor: torch.Tensor, 
                           resonance_tensor: torch.Tensor) -> float:
        """Train network and estimate mutual information"""
        
        # Initialize network
        input_dim = source_tensor.shape[1] + resonance_tensor.shape[1]
        self.network = MINENetwork(input_dim, self.hidden_dim).to(self.device)
        self.optimizer = optim.Adam(self.network.parameters(), lr=self.learning_rate)
        
        # Training data
        joint_samples = torch.cat([source_tensor, resonance_tensor], dim=1)
        marginal_samples = self._generate_marginal_samples(source_tensor, resonance_tensor)
        
        # Training loop
        for epoch in range(self.max_epochs):
            # Forward pass
            joint_output = self.network(joint_samples)
            marginal_output = self.network(marginal_samples)
            
            # MINE objective: E[joint] - log(E[exp(marginal)])
            joint_term = torch.mean(joint_output)
            marginal_term = torch.log(torch.mean(torch.exp(marginal_output)))
            
            # Loss (negative of MINE objective)
            loss = -joint_term + marginal_term
            
            # Backward pass
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            # Record training progress
            if epoch % 100 == 0:
                mi_estimate = joint_term.item() - marginal_term.item()
                self.training_history.append({
                    'epoch': epoch,
                    'loss': loss.item(),
                    'mi_estimate': mi_estimate
                })
        
        # Final estimate
        with torch.no_grad():
            joint_output = self.network(joint_samples)
            marginal_output = self.network(marginal_samples)
            
            joint_term = torch.mean(joint_output)
            marginal_term = torch.log(torch.mean(torch.exp(marginal_output)))
            
            final_mi = joint_term.item() - marginal_term.item()
        
        return max(0, final_mi)  # Mutual information is non-negative
    
    def _generate_marginal_samples(self, source_tensor: torch.Tensor, 
                                  resonance_tensor: torch.Tensor) -> torch.Tensor:
        """Generate marginal samples by shuffling"""
        # Shuffle resonance to break correlation
        shuffled_resonance = resonance_tensor[torch.randperm(len(resonance_tensor))]
        
        # Combine with source
        marginal_samples = torch.cat([source_tensor, shuffled_resonance], dim=1)
        
        return marginal_samples
    
    def _fallback_mi_estimation(self, source: Any, resonance: np.ndarray) -> float:
        """Fallback mutual information estimation"""
        try:
            # Simplified estimation based on correlation
            source_features = self._extract_simple_features(source)
            resonance_features = self._extract_simple_features(resonance)
            
            # Ensure same length
            min_len = min(len(source_features), len(resonance_features))
            source_features = source_features[:min_len]
            resonance_features = resonance_features[:min_len]
            
            # Calculate correlation
            correlation = np.corrcoef(source_features, resonance_features)[0, 1]
            
            if np.isnan(correlation):
                return 0.0
            
            # Convert correlation to mutual information approximation
            # I(X;Y) ≈ -0.5 * log(1 - ρ²) for Gaussian variables
            mi_estimate = -0.5 * np.log(max(1e-10, 1 - correlation**2))
            
            return max(0, mi_estimate)
            
        except:
            return 0.0
    
    def _extract_simple_features(self, data: Any) -> np.ndarray:
        """Extract simple numerical features"""
        if isinstance(data, str):
            return np.array([ord(c) for c in data[:100]])
        elif isinstance(data, (list, np.ndarray)):
            return np.array(data).flatten()[:100]
        else:
            return np.array([hash(str(data)) % 1000])
    
    def get_training_summary(self) -> dict:
        """Get summary of training performance"""
        if not self.training_history:
            return {}
        
        recent = self.training_history[-1]
        return {
            'final_mi_estimate': recent['mi_estimate'],
            'final_loss': recent['loss'],
            'total_epochs': recent['epoch'],
            'convergence': recent['loss'] < 0.1,  # Simple convergence criterion
            'training_history': self.training_history
        }
    
    def reset(self):
        """Reset the estimator state"""
        self.network = None
        self.optimizer = None
        self.training_history = []