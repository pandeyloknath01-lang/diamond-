"""
Professional diamond grading parameters following GIA standards
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DiamondParameters:
    """Complete set of GIA-standard diamond parameters"""
    
    # Basic dimensions (%)
    table_percent: float  # 43-65%
    total_depth_percent: float  # 58-63%
    crown_angle: float  # 30-36°
    pavilion_angle: float  # 40-41°
    crown_height: float  # 7.4-20.8% of table
    pavilion_depth: float  # 42.8-43.8% of depth
    
    # Facet measurements
    star_length: float  # 40-65% of table
    lower_half_length: float  # 70-80% of star
    girdle_thickness_min: float  # % of diameter
    girdle_thickness_max: float  # % of diameter
    culet_size: str  # none/pointed/very_small/small/medium/large/very_large
    
    # Surface quality
    polish: int  # 1-5 (excellent to poor)
    symmetry: int  # 1-5 (excellent to poor)
    painting_digging: int  # 0-5 (none to heavy)
    
    # Diamond properties
    carat_weight: float
    color_grade: str  # D-Z
    clarity_grade: str  # IF-I3
    
    # Fluorescence
    fluorescence: str  # None/Faint/Medium/Strong/Very Strong
    
    def to_dict(self) -> Dict:
        return {
            'table_percent': self.table_percent,
            'total_depth_percent': self.total_depth_percent,
            'crown_angle': self.crown_angle,
            'pavilion_angle': self.pavilion_angle,
            'crown_height': self.crown_height,
            'pavilion_depth': self.pavilion_depth,
            'star_length': self.star_length,
            'lower_half_length': self.lower_half_length,
            'girdle_thickness_min': self.girdle_thickness_min,
            'girdle_thickness_max': self.girdle_thickness_max,
            'culet_size': self.culet_size,
            'polish': self.polish,
            'symmetry': self.symmetry,
            'painting_digging': self.painting_digging,
            'carat_weight': self.carat_weight,
            'color_grade': self.color_grade,
            'clarity_grade': self.clarity_grade,
            'fluorescence': self.fluorescence,
        }


@dataclass
class OpticalMetrics:
    """Optical properties calculated from parameters"""
    light_return: float  # 0-100%
    fire_dispersion: float  # 0-100%
    scintillation: float  # 0-100%
    contrast_pattern: float  # 0-100%
    leakage: float  # 0-100%
    brightness: float  # 0-100%
    
    def overall_score(self) -> float:
        """Weighted average of optical metrics"""
        weights = {
            'light_return': 0.35,
            'fire_dispersion': 0.15,
            'scintillation': 0.20,
            'brightness': 0.15,
            'contrast_pattern': 0.10,
            'leakage': 0.05,
        }
        
        score = (
            self.light_return * weights['light_return'] +
            self.fire_dispersion * weights['fire_dispersion'] +
            self.scintillation * weights['scintillation'] +
            self.brightness * weights['brightness'] +
            self.contrast_pattern * weights['contrast_pattern'] +
            (100 - self.leakage) * weights['leakage']
        )
        return round(score, 2)


@dataclass
class CutGrade:
    """GIA Cut Grade assessment"""
    grade: str  # Excellent, Very Good, Good, Fair, Poor
    reasoning: List[str]
    strength_areas: List[str]
    improvement_areas: List[str]
    predicted_market_value_multiplier: float  # 0.8-1.5x
