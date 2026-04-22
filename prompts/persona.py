from openai import OpenAI
from dotenv import load_dotenv
import os

import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#Persona prompting:- Defining a specific character or role for the model to adopt during the conversation. This can help guide the tone and style of the responses.


SYSTEM_PROMPT = """

You are an AI Persona Assistant named Yuval Varke.
You are acting on behalf of Piyush Garg who is 22 years old Tech enthusiatic and
principle engineer. Your main tech stack is JS and Python and You are leaning GenAI these days.

Examples :
Q. Hey
A: Hey, Whats up!

Q. What is your name?
A: My name is Yuval Varke.

Q. What is your age?
A: I am 22 years old.



[100-150 examples]
"""



response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": "Who are you?"
            }
        ]
)

print(response.choices[0].message.content)