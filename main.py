from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

res = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the capital of India?"
)

print(res.text)

