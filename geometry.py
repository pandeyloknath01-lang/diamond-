import math


def calculate_geometry_metrics(design):
    facet_angle = design.get("facet_angle", 45.0)
    thickness = design.get("thickness", 4.5)
    cut_depth = design.get("cut_depth", 1.2)

    face_area = math.pi * (thickness * 0.7) ** 2
    symmetry = max(0.0, 1.0 - abs(facet_angle - 45.0) / 45.0)
    balance = max(0.0, 1.0 - cut_depth / 3.0)

    return {
        "face_area": round(face_area, 2),
        "symmetry": round(symmetry, 3),
        "balance": round(balance, 3),
        "thickness": round(thickness, 2),
    }
