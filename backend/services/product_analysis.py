import json

from config.settings import PRODUCTS_FILE
from services.price_analysis import analyze_price
from services.seller_analysis import analyze_seller
from services.risk_score import calculate_risk
from services.image_analysis import analyze_image
from services.ocr_analysis import analyze_text
from services.image_similarity import analyze_similarity

from services.product_identity import identify_product
from services.reference_resolver import resolve_reference
from services.reference_repository import list_reference_images


with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
    products = json.load(file)


def analyze_product(product):

    name = product.get("name", "")
    brand = product.get("brand", "")
    price = product.get("price")
    seller = product.get("seller", "")
    image = product.get("image", "")
    color = product.get("color", "")
    specifications = product.get("specifications", "")
    product_identity = identify_product(product)

    reference = resolve_reference(product_identity)


    warnings = []

    image_risk = 20
    brand_risk = 20
    specification_risk = 20
    color_risk = 20
    size_risk = 20

    image_result = {
        "success": False,
        "risk": 70,
        "objects": [],
        "message": "Image unavailable"
    }

    ocr_result = {
        "success": False,
        "text": [],
        "message": "Image unavailable"
    }

    similarity_result = {
        "success": False,
        "similarity": 0,
        "risk": 70,
        "message": "Image unavailable"
    }

    if image:

        image_result = analyze_image(image)

        ocr_result = analyze_text(image)

        reference_images = list_reference_images(product_identity["product_id"])
        if reference_images:
            similarity_result = analyze_similarity(image, reference_images)
        else:
            similarity_result = {
                "success": False,
                "similarity": 0,
                "risk": 0,
                "message": "No product-specific reference images available"
    }

        image_risk = similarity_result["risk"]

        if not similarity_result["success"]:

            warnings.append(
                "CLIP image similarity analysis failed"
            )

    else:

        image_risk = 70

        warnings.append(
            "Product image unavailable"
        )

    if reference:

        expected_brand = reference["brand"]

        if brand:

            if expected_brand.lower() == brand.lower():

                brand_risk = 5

            else:

                brand_risk = 90

                warnings.append(
                    "Brand does not match reference product"
                )

        else:

            brand_risk = 60

            warnings.append(
                "Brand information unavailable"
            )

        reference_price = reference["reference_price"]

        price_result = analyze_price(
            price,
            reference_price
        )

        price_risk = price_result["risk"]

        if price_result["message"]:

            warnings.append(
                price_result["message"]
            )

        if color:

            allowed_colors = reference["allowed_colors"]

            if color.strip().lower() in [c.lower() for c in allowed_colors]:

                color_risk = 5

            else:

                color_risk = 60

                warnings.append(
                    "Unusual product color detected"
                )

    else:

        warnings.append(
            "No reference product found"
        )

        price_result = {
            "risk": 40,
            "difference": None,
            "message": "Reference price unavailable"
        }

        price_risk = 40

    seller_result = analyze_seller(
        seller
    )

    seller_risk = seller_result["risk"]

    if seller_result["message"]:

        warnings.append(
            seller_result["message"]
        )

    if not specifications:

        specification_risk = 60

        warnings.append(
            "Product specifications unavailable"
        )

    result = calculate_risk(
        image_risk,
        brand_risk,
        price_risk,
        seller_risk,
        specification_risk,
        color_risk,
        size_risk
    )

    return {

        "risk_score": result["risk_score"],

        "risk_level": result["risk_level"],

        "features": {

            "image": image_risk,

            "brand_logo": brand_risk,

            "price": price_risk,

            "seller": seller_risk,

            "specifications": specification_risk,

            "color": color_risk,

            "size": size_risk
        },

        "image_analysis": {

            "success": image_result["success"],

            "objects": image_result["objects"],

            "message": image_result["message"]
        },

        "ocr_analysis": {

            "success": ocr_result["success"],

            "text": ocr_result["text"],

            "message": ocr_result.get(
                "message",
                ""
            )
        },

        "similarity_analysis": {

            "success": similarity_result["success"],

            "similarity": similarity_result["similarity"],

            "risk": similarity_result["risk"],

            "message": similarity_result["message"]
        },

        "warnings": warnings
    }