"""
Machine Learning model framework for diamond grading prediction
Trained on GIA-like historical diamond data
"""

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import pickle
from pathlib import Path
from parameters import DiamondParameters, OpticalMetrics
from typing import Tuple, Dict


class DiamondGradingModel:
    """ML model for predicting diamond cut grade"""
    
    def __init__(self, model_path: Path = None):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'table_percent', 'total_depth_percent', 'crown_angle', 'pavilion_angle',
            'crown_height', 'pavilion_depth', 'star_length', 'lower_half_length',
            'girdle_thickness_min', 'girdle_thickness_max', 'polish', 'symmetry',
            'painting_digging', 'carat_weight'
        ]
        
        if model_path and model_path.exists():
            self.load_model(model_path)
    
    def prepare_features(self, params: DiamondParameters) -> np.ndarray:
        """Convert diamond parameters to ML features"""
        features = [
            params.table_percent,
            params.total_depth_percent,
            params.crown_angle,
            params.pavilion_angle,
            params.crown_height,
            params.pavilion_depth,
            params.star_length,
            params.lower_half_length,
            params.girdle_thickness_min,
            params.girdle_thickness_max,
            params.polish,
            params.symmetry,
            params.painting_digging,
            params.carat_weight,
        ]
        return np.array(features).reshape(1, -1)
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the grading model on historical data"""
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Use ensemble for better predictions
        self.model = GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=8,
            random_state=42
        )
        self.model.fit(X_scaled, y)
    
    def predict(self, params: DiamondParameters) -> Tuple[float, Dict]:
        """
        Predict diamond cut grade score (0-100)
        Returns: (score, confidence_dict)
        """
        if self.model is None:
            raise ValueError("Model not trained. Train model first or load from file.")
        
        features = self.prepare_features(params)
        features_scaled = self.scaler.transform(features)
        
        score = self.model.predict(features_scaled)[0]
        score = max(0, min(100, score))
        
        # Get feature importance for interpretation
        importances = self.model.feature_importances_
        top_features = sorted(
            zip(self.feature_names, importances),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        confidence = {
            'score': score,
            'top_factors': [f"{name}: {imp:.3f}" for name, imp in top_features],
            'model_type': 'Gradient Boosting',
        }
        
        return score, confidence
    
    def save_model(self, path: Path):
        """Save trained model"""
        with open(path, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler}, f)
    
    def load_model(self, path: Path):
        """Load trained model"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']


class MarketValuePredictor:
    """Predict market value based on grade and 4Cs"""
    
    def __init__(self):
        self.base_price_per_carat = {
            'D': 8000, 'E': 7500, 'F': 7200,
            'G': 6800, 'H': 6200, 'I': 5500,
            'J': 4800, 'K': 4200, 'L': 3800,
        }
        
        self.clarity_multiplier = {
            'IF': 1.0, 'VVS1': 0.98, 'VVS2': 0.96,
            'VS1': 0.93, 'VS2': 0.90, 'SI1': 0.85,
            'SI2': 0.78, 'I1': 0.70, 'I2': 0.55, 'I3': 0.40,
        }
        
        self.cut_grade_multiplier = {
            'Excellent': 1.15,
            'Very Good': 1.05,
            'Good': 0.95,
            'Fair': 0.80,
            'Poor': 0.60,
        }
        
        self.polish_multiplier = {
            1: 1.05,  # Excellent
            2: 1.00,
            3: 0.95,
            4: 0.85,
            5: 0.70,
        }
    
    def estimate_price(self, params: DiamondParameters, cut_grade: str) -> Dict:
        """Estimate diamond market value"""
        
        base_price = self.base_price_per_carat.get(params.color_grade, 5000)
        clarity_mult = self.clarity_multiplier.get(params.clarity_grade, 0.8)
        cut_mult = self.cut_grade_multiplier.get(cut_grade, 0.9)
        polish_mult = self.polish_multiplier.get(params.polish, 0.85)
        
        price_per_carat = base_price * clarity_mult * cut_mult * polish_mult
        total_price = price_per_carat * params.carat_weight
        
        return {
            'price_per_carat': round(price_per_carat, 2),
            'total_price': round(total_price, 2),
            'currency': 'USD',
            'confidence': 'medium',  # Could be enhanced with real market data
        }
