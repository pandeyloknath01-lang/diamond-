"""
Advanced optical calculations based on diamond geometry
Following ray-tracing principles similar to GIA software
"""

import math
from parameters import DiamondParameters, OpticalMetrics


class DiamondOpticsCalculator:
    """Calculate optical properties from geometric parameters"""
    
    def __init__(self, params: DiamondParameters):
        self.params = params
        self.refractive_index = 2.42  # Diamond's refractive index
    
    def calculate_light_return(self) -> float:
        """
        Calculate light return (brightness)
        Based on table %, depth %, and facet angles
        Optimal range: table 52-58%, depth 60-63%
        """
        # Ideal ranges
        ideal_table_low, ideal_table_high = 52, 58
        ideal_depth_low, ideal_depth_high = 60, 63
        ideal_crown = 33.5
        ideal_pavilion = 40.75
        
        # Calculate deviations
        table_dev = min(
            abs(self.params.table_percent - ideal_table_low),
            abs(self.params.table_percent - ideal_table_high)
        )
        depth_dev = min(
            abs(self.params.total_depth_percent - ideal_depth_low),
            abs(self.params.total_depth_percent - ideal_depth_high)
        )
        crown_dev = abs(self.params.crown_angle - ideal_crown)
        pavilion_dev = abs(self.params.pavilion_angle - ideal_pavilion)
        
        # Calculate light return (0-100%)
        # Perfect parameters = 100%
        light_return = 100 - (
            table_dev * 1.5 +
            depth_dev * 1.2 +
            crown_dev * 2.0 +
            pavilion_dev * 1.8
        )
        
        return max(20, min(100, light_return))
    
    def calculate_fire(self) -> float:
        """
        Calculate fire (chromatic dispersion)
        Based on pavilion angle and table size
        Affected by polish grade
        """
        # Base fire calculation
        ideal_pavilion = 40.75
        pavilion_dev = abs(self.params.pavilion_angle - ideal_pavilion)
        
        fire = 100 - (pavilion_dev * 1.5)
        
        # Polish affects fire perception
        polish_factor = {1: 1.0, 2: 0.95, 3: 0.85, 4: 0.70, 5: 0.50}
        fire *= polish_factor.get(self.params.polish, 0.8)
        
        return max(15, min(100, fire))
    
    def calculate_scintillation(self) -> float:
        """
        Calculate scintillation (sparkle/flashing)
        Based on facet patterns and star/lower half lengths
        Affected by symmetry
        """
        # Optimal facet ratios
        ideal_star = 50  # % of table
        ideal_lower = 75  # % of star
        
        star_dev = abs(self.params.star_length - ideal_star)
        lower_dev = abs(self.params.lower_half_length - ideal_lower)
        
        scintillation = 100 - (star_dev * 0.8 + lower_dev * 0.6)
        
        # Symmetry affects scintillation perception
        symmetry_factor = {1: 1.0, 2: 0.95, 3: 0.80, 4: 0.60, 5: 0.40}
        scintillation *= symmetry_factor.get(self.params.symmetry, 0.7)
        
        return max(10, min(100, scintillation))
    
    def calculate_contrast_pattern(self) -> float:
        """
        Calculate contrast pattern (light/dark areas)
        Based on table size and facet arrangements
        """
        # Optimal contrast occurs around table 54-56%
        ideal_table = 55
        table_dev = abs(self.params.table_percent - ideal_table)
        
        contrast = 100 - (table_dev * 2.0)
        
        # Symmetry and polish affect contrast perception
        symmetry_factor = {1: 1.0, 2: 0.92, 3: 0.75, 4: 0.55, 5: 0.35}
        contrast *= symmetry_factor.get(self.params.symmetry, 0.7)
        
        return max(15, min(100, contrast))
    
    def calculate_leakage(self) -> float:
        """
        Calculate light leakage (dead zones)
        Light that escapes through pavilion instead of returning
        Based on pavilion angle primarily
        """
        ideal_pavilion = 40.75
        pavilion_dev = abs(self.params.pavilion_angle - ideal_pavilion)
        
        # Larger deviations = more leakage
        leakage = pavilion_dev * 2.5
        
        # Depth affects leakage
        ideal_depth = 61.5
        depth_dev = abs(self.params.total_depth_percent - ideal_depth)
        leakage += depth_dev * 1.5
        
        return max(0, min(50, leakage))
    
    def calculate_brightness(self) -> float:
        """
        Calculate overall brightness
        Combination of light return and polish
        """
        light_return = self.calculate_light_return()
        
        polish_factor = {1: 1.0, 2: 0.98, 3: 0.90, 4: 0.75, 5: 0.50}
        brightness = light_return * polish_factor.get(self.params.polish, 0.8)
        
        return brightness
    
    def calculate_all_metrics(self) -> OpticalMetrics:
        """Calculate all optical metrics"""
        return OpticalMetrics(
            light_return=self.calculate_light_return(),
            fire_dispersion=self.calculate_fire(),
            scintillation=self.calculate_scintillation(),
            contrast_pattern=self.calculate_contrast_pattern(),
            leakage=self.calculate_leakage(),
            brightness=self.calculate_brightness(),
        )


def assess_cut_grade(metrics: OpticalMetrics, params: DiamondParameters) -> str:
    """
    Assess cut grade based on optical metrics and parameters
    Similar to GIA's grading system
    """
    score = metrics.overall_score()
    
    # Check parameter compliance
    param_issues = []
    
    if not (52 <= params.table_percent <= 58):
        param_issues.append(f"Table %: {params.table_percent}% (ideal: 52-58%)")
    
    if not (60 <= params.total_depth_percent <= 63):
        param_issues.append(f"Depth %: {params.total_depth_percent}% (ideal: 60-63%)")
    
    if not (33 <= params.crown_angle <= 35):
        param_issues.append(f"Crown angle: {params.crown_angle}° (ideal: 33-35°)")
    
    if not (40 <= params.pavilion_angle <= 41):
        param_issues.append(f"Pavilion angle: {params.pavilion_angle}° (ideal: 40-41°)")
    
    # Grade based on score and parameters
    if score >= 95 and len(param_issues) == 0 and params.polish == 1:
        return "Excellent"
    elif score >= 85 and len(param_issues) <= 1:
        return "Very Good"
    elif score >= 75 and len(param_issues) <= 2:
        return "Good"
    elif score >= 65:
        return "Fair"
    else:
        return "Poor"
