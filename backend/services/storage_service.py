from pathlib import Path
from uuid import uuid4

from config.settings import (
    ANALYSIS_RESULTS_DIR,
    MODELS_DIR,
    REFERENCE_PRODUCTS_DIR,
    UPLOADS_DIR,
)


def _save_bytes(data: bytes, directory: Path, filename: str | None = None) -> str:
    directory.mkdir(parents=True, exist_ok=True)

    if filename:
        safe_name = Path(filename).name
        output_path = directory / safe_name
    else:
        output_path = directory / str(uuid4())

    output_path.write_bytes(data)

    return str(output_path)


def save_upload(data: bytes, filename: str | None = None) -> str:
    return _save_bytes(data, UPLOADS_DIR, filename)


def save_reference_product(data: bytes, filename: str | None = None) -> str:
    return _save_bytes(data, REFERENCE_PRODUCTS_DIR, filename)


def save_analysis_result(data: bytes, filename: str | None = None) -> str:
    return _save_bytes(data, ANALYSIS_RESULTS_DIR, filename)


def save_model(data: bytes, filename: str | None = None) -> str:
    return _save_bytes(data, MODELS_DIR, filename)
