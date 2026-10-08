import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import requests
from io import BytesIO
import os


model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
)

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)


def get_image_embedding(image):

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model.vision_model(
            pixel_values=inputs["pixel_values"]
        )

        pooled_output = outputs.pooler_output

        features = model.visual_projection(
            pooled_output
        )

    features = features / features.norm(
        dim=-1,
        keepdim=True
    )

    return features


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


def load_reference_images():

    folder = "reference_images"

    images = []

    for filename in os.listdir(folder):

        if filename.lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp")
        ):

            path = os.path.join(
                folder,
                filename
            )

            image = Image.open(
                path
            ).convert("RGB")

            images.append(image)

    return images


def analyze_similarity(image_source):

    try:

        product_image = load_image(
            image_source
        )

        references = load_reference_images()

        if not references:

            return {
                "success": False,
                "similarity": 0,
                "risk": 70,
                "message": "No reference images found"
            }

        product_embedding = get_image_embedding(
            product_image
        )

        best_similarity = 0

        for reference in references:

            reference_embedding = (
                get_image_embedding(reference)
            )

            similarity = torch.cosine_similarity(
                product_embedding,
                reference_embedding
            ).item()

            if similarity > best_similarity:

                best_similarity = similarity

        similarity_percentage = round(
            best_similarity * 100,
            2
        )

        if similarity_percentage >= 90:
            risk = 10

        elif similarity_percentage >= 75:
            risk = 30

        elif similarity_percentage >= 60:
            risk = 60

        else:
            risk = 90

        return {
            "success": True,
            "similarity": similarity_percentage,
            "risk": risk,
            "message": "Image similarity analyzed"
        }

    except Exception as error:

        return {
            "success": False,
            "similarity": 0,
            "risk": 70,
            "message": str(error)
        }