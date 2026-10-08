import json
from pathlib import Path

from config.settings import REFERENCE_PRODUCTS_DIR


def save_product_metadata(product_id: str, metadata: dict) -> str:
    product_dir = REFERENCE_PRODUCTS_DIR / product_id
    product_dir.mkdir(parents=True, exist_ok=True)

    metadata_path = product_dir / "metadata.json"

    metadata_path.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    return str(metadata_path)


def load_product_metadata(product_id: str) -> dict | None:
    metadata_path = REFERENCE_PRODUCTS_DIR / product_id / "metadata.json"

    if not metadata_path.exists():
        return None

    return json.loads(
        metadata_path.read_text(encoding="utf-8")
    )