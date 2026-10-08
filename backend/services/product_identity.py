def identify_product(product):
    name = product.get("name", "").strip()
    brand = product.get("brand", "").strip()
    specifications = product.get("specifications", "").strip()

    return {
        "name": name,
        "brand": brand,
        "specifications": specifications,
    }