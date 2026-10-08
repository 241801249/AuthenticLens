from services.image_analysis import analyze_image
from services.ocr_analysis import analyze_text
from services.image_similarity import analyze_similarity

image_path = "reference_images/nike_air_max_270_1.jpg"

print("\n===== YOLO =====")
print(analyze_image(image_path))

print("\n===== OCR =====")
print(analyze_text(image_path))

print("\n===== CLIP =====")
print(analyze_similarity(image_path))