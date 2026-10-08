def analyze_price(current_price, reference_price):

    if current_price is None or reference_price is None:
        return {
            "risk": 50,
            "difference": None,
            "message": "Price information unavailable"
        }

    try:
        current_price = float(current_price)
        reference_price = float(reference_price)
    except (TypeError, ValueError):
        return {
            "risk": 50,
            "difference": None,
            "message": "Price information is invalid"
        }

    if reference_price <= 0 or current_price < 0:
        return {
            "risk": 50,
            "difference": None,
            "message": "Price information is invalid"
        }

    difference = ((reference_price - current_price) / reference_price) * 100

    if difference >= 60:
        risk = 90
        message = "Price is significantly below the reference price"

    elif difference >= 40:
        risk = 70
        message = "Price is unusually low"

    elif difference >= 20:
        risk = 40
        message = "Price is moderately below the reference price"

    else:
        risk = 10
        message = "Price is within the expected range"

    return {
        "risk": round(risk),
        "difference": round(difference, 2),
        "message": message
    }