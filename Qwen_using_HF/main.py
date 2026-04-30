from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv(override=True)

client = InferenceClient(
    api_key=os.getenv("HF_TOKEN"),
)

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct:together",
    messages=[
        {"role": "user", "content": "Explain the book Homo Sapiens by Yuval Noah Harari in one sentence"}
    ],
    max_tokens=100,
)

print(response.choices[0].message.content)