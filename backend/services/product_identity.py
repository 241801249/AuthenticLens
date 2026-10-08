import re


def identify_product(product):
    name = product.get("name", "").strip()
    brand = product.get("brand", "").strip()
    specifications = product.get("specifications", "").strip()

    normalized_name = name.lower()

    if brand and normalized_name.startswith(brand.lower()):
        identity_text = normalized_name
    else:
        identity_text = f"{brand} {normalized_name}".strip()

    product_id = re.sub(r"[^a-z0-9]+", "-", identity_text)
    product_id = product_id.strip("-")

    return {
        "product_id": product_id,
        "name": name,
        "brand": brand,
        "specifications": specifications,
    }