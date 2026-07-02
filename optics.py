def analyze_optics(design):
    facet_angle = design.get("facet_angle", 45.0)
    surface_quality = design.get("surface_quality", 0.8)
    cut_depth = design.get("cut_depth", 1.2)

    brilliance = 0.5 * surface_quality + 0.3 * (1.0 - abs(facet_angle - 45.0) / 45.0) + 0.2 * (1.0 - cut_depth / 3.0)
    dispersion = round(0.55 + 0.25 * surface_quality, 3)

    return {
        "brilliance": round(brilliance, 3),
        "dispersion": dispersion,
        "surface_quality": round(surface_quality, 3),
    }
