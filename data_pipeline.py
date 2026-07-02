"""
Data pipeline for diamond grading
Handles data loading, preprocessing, and synthetic data generation
"""

import pandas as pd
import numpy as np
from pathlib import Path
from parameters import DiamondParameters
from typing import List, Tuple


class DiamondDataGenerator:
    """Generate synthetic GIA-like diamond data for training"""
    
    @staticmethod
    def generate_synthetic_dataset(n_samples: int = 5000) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Generate synthetic diamond dataset similar to GIA grading records
        
        Args:
            n_samples: Number of synthetic diamonds to generate
            
        Returns:
            (DataFrame with parameters, Series with cut grades)
        """
        np.random.seed(42)
        
        data = {
            'table_percent': np.random.normal(55, 2.5, n_samples),
            'total_depth_percent': np.random.normal(61.5, 1.5, n_samples),
            'crown_angle': np.random.normal(33.5, 1.2, n_samples),
            'pavilion_angle': np.random.normal(40.75, 0.8, n_samples),
            'crown_height': np.random.normal(14, 2, n_samples),
            'pavilion_depth': np.random.normal(43.3, 1.5, n_samples),
            'star_length': np.random.normal(50, 5, n_samples),
            'lower_half_length': np.random.normal(75, 5, n_samples),
            'girdle_thickness_min': np.random.uniform(0.5, 1.5, n_samples),
            'girdle_thickness_max': np.random.uniform(1.5, 3.5, n_samples),
            'polish': np.random.randint(1, 6, n_samples),
            'symmetry': np.random.randint(1, 6, n_samples),
            'painting_digging': np.random.randint(0, 4, n_samples),
            'carat_weight': np.random.uniform(0.5, 5.0, n_samples),
            'color_grade': np.random.choice(['D', 'E', 'F', 'G', 'H', 'I', 'J'], n_samples),
            'clarity_grade': np.random.choice(['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2'], n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Generate synthetic grades based on parameters
        grades = []
        for idx, row in df.iterrows():
            score = DiamondDataGenerator._calculate_grade_score(row)
            if score >= 95:
                grades.append('Excellent')
            elif score >= 85:
                grades.append('Very Good')
            elif score >= 75:
                grades.append('Good')
            elif score >= 65:
                grades.append('Fair')
            else:
                grades.append('Poor')
        
        df['cut_grade'] = grades
        
        # Create grade numeric values for ML
        grade_map = {'Excellent': 95, 'Very Good': 85, 'Good': 75, 'Fair': 65, 'Poor': 55}
        grade_scores = pd.Series([grade_map[g] for g in grades])
        
        # Clamp values
        df = df.clip(lower=df.min() * 0.8, upper=df.max() * 1.2)
        
        return df, grade_scores
    
    @staticmethod
    def _calculate_grade_score(row) -> float:
        """Calculate diamond grade score from parameters"""
        
        # Calculate deviations from ideal
        table_ideal = 55
        table_dev = abs(row['table_percent'] - table_ideal)
        
        depth_ideal = 61.5
        depth_dev = abs(row['total_depth_percent'] - depth_ideal)
        
        crown_ideal = 33.5
        crown_dev = abs(row['crown_angle'] - crown_ideal)
        
        pavilion_ideal = 40.75
        pavilion_dev = abs(row['pavilion_angle'] - pavilion_ideal)
        
        # Calculate score
        score = 100 - (
            table_dev * 1.5 +
            depth_dev * 1.2 +
            crown_dev * 2.0 +
            pavilion_dev * 1.8
        )
        
        # Apply polish and symmetry penalties
        polish_factor = {1: 0, 2: -2, 3: -8, 4: -15, 5: -30}
        symmetry_factor = {1: 0, 2: -2, 3: -8, 4: -15, 5: -25}
        
        score += polish_factor.get(row['polish'], -10)
        score += symmetry_factor.get(row['symmetry'], -10)
        
        return max(0, min(100, score))
    
    @staticmethod
    def load_csv_dataset(filepath: Path) -> Tuple[pd.DataFrame, pd.Series]:
        """Load real diamond dataset from CSV"""
        df = pd.read_csv(filepath)
        
        # Extract features and target
        if 'cut_grade' in df.columns:
            grades = df['cut_grade']
            grade_map = {'Excellent': 95, 'Very Good': 85, 'Good': 75, 'Fair': 65, 'Poor': 55}
            target = pd.Series([grade_map.get(g, 70) for g in grades])
        else:
            # Assume last column is target
            target = df.iloc[:, -1]
        
        features = df.drop('cut_grade', axis=1, errors='ignore')
        
        return features, target


class DataPreprocessor:
    """Preprocess diamond data for ML models"""
    
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate diamond data"""
        df = df.copy()
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.fillna(df.mean(numeric_only=True))
        
        # Remove outliers (values outside 3 sigma)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            df = df[np.abs((df[col] - mean) / std) <= 3]
        
        return df
    
    @staticmethod
    def validate_parameters(params: DiamondParameters) -> Tuple[bool, List[str]]:
        """Validate diamond parameters against GIA specifications"""
        issues = []
        
        # Table percentage
        if not (43 <= params.table_percent <= 65):
            issues.append(f"Table %: {params.table_percent} (valid: 43-65)")
        
        # Total depth
        if not (58 <= params.total_depth_percent <= 66):
            issues.append(f"Total depth %: {params.total_depth_percent} (valid: 58-66)")
        
        # Crown angle
        if not (30 <= params.crown_angle <= 36):
            issues.append(f"Crown angle: {params.crown_angle}° (valid: 30-36°)")
        
        # Pavilion angle
        if not (38 <= params.pavilion_angle <= 42):
            issues.append(f"Pavilion angle: {params.pavilion_angle}° (valid: 38-42°)")
        
        # Polish and symmetry
        if not (1 <= params.polish <= 5):
            issues.append(f"Polish: {params.polish} (valid: 1-5)")
        
        if not (1 <= params.symmetry <= 5):
            issues.append(f"Symmetry: {params.symmetry} (valid: 1-5)")
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    @staticmethod
    def export_dataset(df: pd.DataFrame, filepath: Path):
        """Export dataset to CSV"""
        df.to_csv(filepath, index=False)
        print(f"Dataset exported to {filepath}")
    
    @staticmethod
    def generate_training_csv(output_path: Path, n_samples: int = 5000):
        """Generate and save synthetic training dataset"""
        df, grades = DiamondDataGenerator.generate_synthetic_dataset(n_samples)
        df['grade_score'] = grades
        
        DataPreprocessor.export_dataset(df, output_path)
        return df
