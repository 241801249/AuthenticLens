from pathlib import Path


# Project directories
BACKEND_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BACKEND_DIR / "data"
REFERENCE_IMAGES_DIR = BACKEND_DIR / "reference_images"

# Reference product database
PRODUCTS_FILE = DATA_DIR / "products.json"

# YOLO model
YOLO_MODEL_FILE = BACKEND_DIR / "yolo26n.pt"
# Local storage directories
STORAGE_DIR = BACKEND_DIR / "storage"
REFERENCE_PRODUCTS_DIR = STORAGE_DIR / "reference_products"
ANALYSIS_RESULTS_DIR = STORAGE_DIR / "analysis_results"
UPLOADS_DIR = STORAGE_DIR / "uploads"
MODELS_DIR = STORAGE_DIR / "models"
