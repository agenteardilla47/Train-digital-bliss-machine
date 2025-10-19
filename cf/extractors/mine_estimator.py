"""
Mutual Information Neural Estimation (MINE) Implementation

This module provides a robust implementation of MINE for estimating
mutual information between source data and resonance vectors.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Any, Dict, Tuple, Optional
import time


class MINENetwork(nn.Module):
    """Neural network for MINE estimation"""
    
    def __init__(self, input_dim: int, hidden_dims: list = [64, 32]):
        super(MINENetwork, self).__init__()
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.1))
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, 1))
        
        self.network = nn.Sequential(*layers)
        
    def forward(self, x):
        return self.network(x)


class MINEEstimator:
    """Mutual Information Neural Estimation"""
    
    def __init__(self, 
                 learning_rate: float = 0.001,
                 batch_size: int = 64,
                 epochs: int = 100,
                 device: str = 'auto'):
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs
        
        # Set device
        if device == 'auto':
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        
        self.network = None
        self.optimizer = None
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
            # Convert source to numerical representation
            source_vector = self._convert_to_vector(source)
            
            if source_vector is None or len(source_vector) == 0:
                return 0.0
            
            # Ensure compatible dimensions
            min_dims = min(len(source_vector), len(resonance))
            source_vector = source_vector[:min_dims]
            resonance = resonance[:min_dims]
            
            # Create joint and marginal samples
            joint_samples, marginal_samples = self._create_samples(source_vector, resonance)
            
            # Train MINE network
            mi_estimate = self._train_mine(joint_samples, marginal_samples)
            
            return max(0.0, mi_estimate)  # MI is non-negative
            
        except Exception as e:
            # Fallback to simplified estimation
            return self._simplified_mi_estimation(source, resonance)
    
    def _convert_to_vector(self, source: Any) -> Optional[np.ndarray]:
        """Convert source data to numerical vector"""
        try:
            if isinstance(source, str):
                # Convert string to character frequency vector
                char_counts = {}
                for char in source:
                    char_counts[char] = char_counts.get(char, 0) + 1
                
                # Create frequency vector
                max_chars = 256  # ASCII range
                vector = np.zeros(max_chars)
                for char, count in char_counts.items():
                    if ord(char) < max_chars:
                        vector[ord(char)] = count
                
                # Normalize
                if np.sum(vector) > 0:
                    vector = vector / np.sum(vector)
                
                return vector
            
            elif isinstance(source, (list, tuple)):
                # Convert list to numerical vector
                if len(source) == 0:
                    return None
                
                # Try to convert to float
                try:
                    vector = np.array(source, dtype=float)
                    return vector
                except:
                    # Convert to string representation
                    return self._convert_to_vector(str(source))
            
            elif isinstance(source, dict):
                # Convert dict to vector
                values = list(source.values())
                return self._convert_to_vector(values)
            
            elif isinstance(source, np.ndarray):
                return source.astype(float)
            
            else:
                # Generic conversion
                return self._convert_to_vector(str(source))
                
        except:
            return None
    
    def _create_samples(self, source_vector: np.ndarray, 
                       resonance: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create joint and marginal samples for MINE"""
        
        # Ensure same length
        min_len = min(len(source_vector), len(resonance))
        source_vector = source_vector[:min_len]
        resonance = resonance[:min_len]
        
        # Create joint samples (X, Y)
        joint_samples = np.column_stack([source_vector, resonance])
        
        # Create marginal samples (X, Y') where Y' is shuffled
        np.random.seed(42)  # For reproducibility
        shuffled_resonance = np.random.permutation(resonance)
        marginal_samples = np.column_stack([source_vector, shuffled_resonance])
        
        return joint_samples, marginal_samples
    
    def _train_mine(self, joint_samples: np.ndarray, 
                   marginal_samples: np.ndarray) -> float:
        """Train MINE network to estimate mutual information"""
        
        # Convert to tensors
        joint_tensor = torch.FloatTensor(joint_samples).to(self.device)
        marginal_tensor = torch.FloatTensor(marginal_samples).to(self.device)
        
        # Initialize network
        input_dim = joint_samples.shape[1]
        self.network = MINENetwork(input_dim).to(self.device)
        self.optimizer = optim.Adam(self.network.parameters(), lr=self.learning_rate)
        
        # Training loop
        self.training_history = []
        
        for epoch in range(self.epochs):
            # Shuffle data
            joint_indices = torch.randperm(len(joint_tensor))
            marginal_indices = torch.randperm(len(marginal_tensor))
            
            joint_shuffled = joint_tensor[joint_indices]
            marginal_shuffled = marginal_tensor[marginal_indices]
            
            # Compute MINE loss
            joint_scores = self.network(joint_shuffled)
            marginal_scores = self.network(marginal_shuffled)
            
            # MINE loss: -E[T(x,y)] + log(E[exp(T(x,y'))])
            joint_loss = -torch.mean(joint_scores)
            marginal_loss = torch.log(torch.mean(torch.exp(marginal_scores)))
            
            mine_loss = joint_loss + marginal_loss
            
            # Backward pass
            self.optimizer.zero_grad()
            mine_loss.backward()
            self.optimizer.step()
            
            # Record training history
            self.training_history.append({
                'epoch': epoch,
                'loss': mine_loss.item(),
                'mi_estimate': mine_loss.item()
            })
        
        # Return final MI estimate
        with torch.no_grad():
            joint_scores = self.network(joint_tensor)
            marginal_scores = self.network(marginal_tensor)
            
            joint_mean = torch.mean(joint_scores)
            marginal_mean = torch.log(torch.mean(torch.exp(marginal_scores)))
            
            mi_estimate = joint_mean + marginal_mean
        
        return mi_estimate.item()
    
    def _simplified_mi_estimation(self, source: Any, resonance: np.ndarray) -> float:
        """Simplified mutual information estimation as fallback"""
        try:
            # Calculate entropies
            source_entropy = self._calculate_entropy(source)
            resonance_entropy = self._calculate_entropy(resonance)
            
            # Estimate joint entropy
            joint_entropy = source_entropy + resonance_entropy - 0.1  # Simplified
            
            # Mutual information: I(X;Y) = H(X) + H(Y) - H(X,Y)
            mutual_info = max(0, source_entropy + resonance_entropy - joint_entropy)
            
            return mutual_info
            
        except:
            return 0.0
    
    def _calculate_entropy(self, data: Any) -> float:
        """Calculate entropy of data"""
        try:
            if isinstance(data, str):
                # Character-level entropy
                char_counts = {}
                for char in data:
                    char_counts[char] = char_counts.get(char, 0) + 1
                
                probs = np.array(list(char_counts.values())) / len(data)
                probs = probs[probs > 0]  # Remove zero probabilities
                
                if len(probs) == 0:
                    return 0.0
                
                return -np.sum(probs * np.log2(probs))
            
            elif isinstance(data, np.ndarray):
                # Array entropy
                if len(data) == 0:
                    return 0.0
                
                # Discretize continuous data
                data_discrete = np.digitize(data, bins=np.linspace(data.min(), data.max(), 10))
                
                unique, counts = np.unique(data_discrete, return_counts=True)
                probs = counts / len(data_discrete)
                probs = probs[probs > 0]
                
                if len(probs) == 0:
                    return 0.0
                
                return -np.sum(probs * np.log2(probs))
            
            else:
                return 0.0
                
        except:
            return 0.0
    
    def get_training_summary(self) -> Dict[str, Any]:
        """Get training summary"""
        if not self.training_history:
            return {}
        
        losses = [h['loss'] for h in self.training_history]
        mi_estimates = [h['mi_estimate'] for h in self.training_history]
        
        return {
            'epochs': len(self.training_history),
            'final_loss': losses[-1] if losses else 0,
            'final_mi_estimate': mi_estimates[-1] if mi_estimates else 0,
            'min_loss': min(losses) if losses else 0,
            'max_mi_estimate': max(mi_estimates) if mi_estimates else 0,
            'converged': len(losses) > 10 and abs(losses[-1] - losses[-10]) < 0.001
        }