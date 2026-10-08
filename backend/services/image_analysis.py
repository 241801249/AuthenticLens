from ultralytics import YOLO
from PIL import Image
from io import BytesIO
import requests
import os


model = YOLO("yolo26n.pt")


def load_image(image_source):

    if image_source.startswith("http://") or image_source.startswith("https://"):

        response = requests.get(
            image_source,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        return Image.open(
            BytesIO(response.content)
        ).convert("RGB")

    if os.path.exists(image_source):

        return Image.open(
            image_source
        ).convert("RGB")

    raise ValueError(
        "Image file or URL not found"
    )


def analyze_image(image_source):

    if not image_source:

        return {
            "success": False,
            "risk": 70,
            "objects": [],
            "message": "Image unavailable"
        }

    try:

        image = load_image(
            image_source
        )

        results = model(image)

        objects = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                class_id = int(
                    box.cls[0]
                )

                confidence = float(
                    box.conf[0]
                )

                class_name = result.names[
                    class_id
                ]

                objects.append({
                    "object": class_name,
                    "confidence": round(
                        confidence * 100,
                        2
                    )
                })

        if objects:

            risk = 15
            message = "Product image successfully analyzed"

        else:

            risk = 50
            message = "No recognizable object detected"

        return {
            "success": True,
            "risk": risk,
            "objects": objects,
            "message": message
        }

    except Exception as error:

        return {
            "success": False,
            "risk": 60,
            "objects": [],
            "message": str(error)
        }