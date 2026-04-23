from google import genai
from dotenv import load_dotenv
import os
import requests
import json
import re

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ------------------ TOOL ------------------
def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    response.encoding = "utf-8"

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

    return "Something went wrong"


available_tools = {
    "get_weather": get_weather
}

# ------------------ SYSTEM PROMPT ------------------
SYSTEM_PROMPT = """
You are a structured AI agent.

Execution flow:
START → PLAN → TOOL → OBSERVE → PLAN → OUTPUT

Rules:
- STRICT JSON only (no markdown, no ``` blocks)
- Only ONE step at a time
- Never skip steps
- After OUTPUT → STOP
- Never repeat same tool call with same input
- Never change user request
- Never introduce new cities

Capabilities:
- You ONLY have access to CURRENT weather
- You CANNOT predict future weather

If request cannot be fulfilled:
→ Go directly to OUTPUT explaining limitation

JSON format:
{
  "step": "START" | "PLAN" | "TOOL" | "OBSERVE" | "OUTPUT",
  "content": "string",
  "tool": "string",
  "input": "string"
}

Available tool:
get_weather(city: str)

Example:

User: What is the weather in Ahmedabad and Indore?

{ "step": "START", "content": "User wants weather for Ahmedabad and Indore." }

{ "step": "PLAN", "content": "Fetch weather for Ahmedabad." }

{ "step": "TOOL", "tool": "get_weather", "input": "Ahmedabad" }

{ "step": "PLAN", "content": "Fetch weather for Indore." }

{ "step": "TOOL", "tool": "get_weather", "input": "Indore" }

{ "step": "PLAN", "content": "All data collected." }

{ "step": "OUTPUT", "content": "Ahmedabad: <weather>, Indore: <weather>" }
"""

# ------------------ HELPERS ------------------
def clean_json(text):
    if text is None:
        return None
    text = re.sub(r"```json\s*|\s*```", "", text.strip())
    return text


# ------------------ MAIN ------------------
def main():
    while True:
        user_query = input("👉 ")

        message_history = SYSTEM_PROMPT + f"\nUser: {user_query}\n"

        MAX_STEPS = 15
        steps = 0
        called_cities = set()

        while True:
            steps += 1

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=message_history
            )

            raw_result = response.text

            if raw_result is None:
                print("⚠️ Empty response.")
                break

            cleaned = clean_json(raw_result)

            try:
                parsed = json.loads(cleaned)
            except Exception:
                print("⚠️ Invalid JSON:\n", raw_result)
                break

            step = parsed.get("step")

            # -------- HANDLE STEPS --------
            if step == "START":
                print("🔥", parsed.get("content"))

            elif step == "PLAN":
                print("🧠", parsed.get("content"))

            elif step == "TOOL":
                tool = parsed.get("tool")
                city = parsed.get("input")

                # prevent duplicate calls
                if city in called_cities:
                    print(f"⚠️ Already fetched {city}, skipping.")
                    continue

                called_cities.add(city)

                print(f"🛠️ : {tool} ({city})")

                result = available_tools[tool](city)

                print(f"🛠️ : {tool} ({city}) = {result}")

                observation = {
                    "step": "OBSERVE",
                    "tool": tool,
                    "content": result
                }

                message_history += f"\n{json.dumps(observation)}\n"
                continue

            elif step == "OUTPUT":
                print("🤖", parsed.get("content"))
                break

            # append assistant step
            message_history += f"\n{cleaned}\n"

        print("\n\n")


if __name__ == "__main__":
    main()