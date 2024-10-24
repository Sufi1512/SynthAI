import requests
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

# Query the image generation API
image_bytes = query({
    "inputs": "Astronaut riding a horse",
})

# Display the image using PIL
image = Image.open(io.BytesIO(image_bytes))
image.show()  # This will open the image in the default image viewer
