from dotenv import load_dotenv
load_dotenv()

from google import genai
import os
import requests
from PIL import Image
from io import BytesIO

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

url1 = "https://images.pexels.com/photos/7988116/pexels-photo-7988116.jpeg"

# STEP 1: download image
response = requests.get(url1)
img = Image.open(BytesIO(response.content))

# STEP 2: send image + prompt
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "Describe the image in short.",
        img
    ]
)

print(response.text)