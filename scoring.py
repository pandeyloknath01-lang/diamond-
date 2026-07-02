def score_design(geometry, optics):
    symmetry = geometry.get("symmetry", 0.0)
    balance = geometry.get("balance", 0.0)
    brilliance = optics.get("brilliance", 0.0)

    score = (symmetry * 0.35 + balance * 0.25 + brilliance * 0.40) * 100
    return round(score, 1)
