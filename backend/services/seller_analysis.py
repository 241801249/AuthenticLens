def analyze_seller(seller):

    if not seller:
        return {
            "risk": 60,
            "message": "Seller information unavailable"
        }

    seller_text = seller.lower()

    if "official" in seller_text:
        return {
            "risk": 5,
            "message": "Official seller detected"
        }

    if "authorized" in seller_text:
        return {
            "risk": 10,
            "message": "Authorized seller detected"
        }

    return {
        "risk": 35,
        "message": "Seller requires further verification"
    }