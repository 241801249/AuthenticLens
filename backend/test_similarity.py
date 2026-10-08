from services.image_similarity import (
    get_image_embedding
)

from PIL import Image
import torch


reference1 = Image.open(
    "reference_images/nike_air_max_270_1.jpg"
).convert("RGB")

reference2 = Image.open(
    "reference_images/nike_air_max_270_2.jpg"
).convert("RGB")


embedding1 = get_image_embedding(
    reference1
)

embedding2 = get_image_embedding(
    reference2
)


similarity = torch.cosine_similarity(
    embedding1,
    embedding2
).item()


similarity_percentage = round(
    similarity * 100,
    2
)


print(
    "Image Similarity:",
    similarity_percentage,
    "%"
)