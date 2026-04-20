from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

messages = []

while True:
    user_input = input("Enter your question: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({
        "role":"user",
        "content":user_input
    })
    
    res = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=list(map(lambda message:message["role"] + " : " + message["content"], messages)),
    )

    messages.append({
        "role":"AI Assistant",
        "content":res.text
    })
    print(res.text)

