def calculate_risk(
    image_risk,
    brand_risk,
    price_risk,
    seller_risk,
    specification_risk,
    color_risk,
    size_risk
):

    risk = (
        image_risk * 0.25 +
        brand_risk * 0.15 +
        price_risk * 0.20 +
        seller_risk * 0.15 +
        specification_risk * 0.10 +
        color_risk * 0.05 +
        size_risk * 0.10
    )

    risk = round(risk)

    if risk <= 20:
        level = "LOW"
    elif risk <= 40:
        level = "MEDIUM"
    elif risk <= 70:
        level = "HIGH"
    else:
        level = "VERY HIGH"

    return {
        "risk_score": risk,
        "risk_level": level
    }