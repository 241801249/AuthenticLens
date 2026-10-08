from services.product_repository import load_product_metadata


def resolve_reference(product_identity):
    product_id = product_identity.get("product_id")

    if not product_id:
        return None

    return load_product_metadata(product_id)