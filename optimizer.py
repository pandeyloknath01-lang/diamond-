def optimize_design(geometry, optics, score):
    suggested_angle = 45.0 + (100.0 - score) / 20.0
    suggested_angle = max(25.0, min(70.0, suggested_angle))

    return {
        "suggested_angle": round(suggested_angle, 1),
        "recommended_quality": round(min(1.0, optics["surface_quality"] + 0.05), 3),
    }
