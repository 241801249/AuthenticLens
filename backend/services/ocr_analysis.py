import easyocr
import numpy as np
import requests
import os

from PIL import Image
from io import BytesIO


reader = easyocr.Reader(
    ["en"],
    gpu=False
)


def analyze_text(image_source):

    if not image_source:

        return {
            "success": False,
            "text": [],
            "message": "Image unavailable"
        }

    try:

        if image_source.startswith("http://") or image_source.startswith("https://"):

            response = requests.get(
                image_source,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            response.raise_for_status()

            image = Image.open(
                BytesIO(response.content)
            ).convert("RGB")

        else:

            if not os.path.exists(image_source):

                return {
                    "success": False,
                    "text": [],
                    "message": "Image file not found"
                }

            image = Image.open(
                image_source
            ).convert("RGB")

        image_array = np.array(image)

        result = reader.readtext(
            image_array
        )

        detected_text = []

        for item in result:

            detected_text.append({
                "text": item[1],
                "confidence": round(
                    float(item[2]) * 100,
                    2
                )
            })

        return {
            "success": True,
            "text": detected_text,
            "message": "Text detection completed"
        }

    except Exception as error:

        return {
            "success": False,
            "text": [],
            "message": str(error)
        }