from pathlib import Path

from config.settings import REFERENCE_PRODUCTS_DIR


def get_product_directory(product_id: str) -> Path:
    product_dir = REFERENCE_PRODUCTS_DIR / product_id
    product_dir.mkdir(parents=True, exist_ok=True)
    return product_dir


def save_reference_image(
    product_id: str,
    image_data: bytes,
    filename: str,
) -> str:
    product_dir = get_product_directory(product_id)

    safe_filename = Path(filename).name
    image_path = product_dir / safe_filename

    image_path.write_bytes(image_data)

    return str(image_path)


def list_reference_images(product_id: str) -> list[str]:
    product_dir = REFERENCE_PRODUCTS_DIR / product_id

    if not product_dir.exists():
        return []

    return [
    str(path)
    for path in product_dir.iterdir()
    if path.is_file()
    and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]