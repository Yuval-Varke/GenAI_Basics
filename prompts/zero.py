from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#Zero-shot prompting:- Directly asking the model to perform a task without providing any examples or context. The model relies solely on its pre-existing knowledge and understanding to generate a response.

SYSTEM_PROMPT = "You should answer only and only coding related problems. Your name is Alexa. If user asks something other than coding, just say sorry."

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {   "role": "system",
            "content": SYSTEM_PROMPT
        },
        # {
        #     "role": "user",
        #     "content": "What is the capital of France?"
        # },
        {
            "role": "user",
            "content": "Write a Python function to calculate the factorial of a number."
        }
    ]
)

print(response.choices[0].message.content)