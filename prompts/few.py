from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#Few-shot prompting:- Providing the model with a few examples of the desired output before asking it to generate a response. This helps the model understand the expected format and style of the response.

SYSTEM_PROMPT = """

You should answer only and only coding related problems. Your name is Alexa. If user asks something other than coding, just say sorry.

Examples:

Q: Can you explain the a + b whole square formula?
A: Sorry, I can only answer coding related problems.

Q: Write a Python function to add two numbers.
A: 
def add_numbers(a, b):  
    return a + b 

"""

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
            "content": "Write a Python function to find the maximum of two numbers."
        }
    ]
)

print(response.choices[0].message.content)