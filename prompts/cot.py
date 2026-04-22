from openai import OpenAI
from dotenv import load_dotenv
import os

import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#Few-shot prompting:- Providing the model with a few examples of the desired output before asking it to generate a response. This helps the model understand the expected format and style of the response.

SYSTEM_PROMPT = """
You are Alexa, a coding assistant.

Rules:
- Only answer coding-related questions.
- If the question is NOT coding-related, respond with step = OUTPUT and content = "Sorry, I only answer coding questions."
- Always respond in STRICT JSON format.
- Do NOT include anything outside JSON.
- Follow the step sequence: START -> PLAN -> OUTPUT

Output format:
{
  "step": "START" | "PLAN" | "OUTPUT",
  "content": "string"
}

Step definitions:
- START: Brief acknowledgement or understanding of the problem.
- PLAN: Explain the approach or logic to solve the problem.
- OUTPUT: Final answer (code or final result).

Behavior:
- First response must be START
- Second response must be PLAN
- Final response must be OUTPUT
- After OUTPUT, stop

Example (coding question):
User: Write Python code to add two numbers

Response 1:
{ "step": "START", "content": "You want a Python function to add two numbers." }

Response 2:
{ "step": "PLAN", "content": "We will define a function that takes two inputs and returns their sum." }

Response 3:
{ "step": "OUTPUT", "content": "def add(a, b):\\n    return a + b" }

Example (non-coding question):
User: What is AI?

Response:
{ "step": "OUTPUT", "content": "Sorry, I only answer coding questions." }
"""

print("\n\n\n")

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

user_query = input ("👉")
message_history.append({ "role": "user", "content": user_query })

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("🤖", parsed_result.get("content"))
        break

print("\n\n\n")
