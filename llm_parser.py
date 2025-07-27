# import os
# import openai
# from dotenv import load_dotenv

# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def parse_meeting_prompt(prompt: str) -> dict:
#     system_prompt = "Extract meeting details like title, date, time, duration (in minutes), and participants from the input."
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     try:
#         result = eval(response.choices[0].message.content.strip())
#         return result
#     except:
#         return {}


import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def parse_meeting_prompt(prompt: str) -> dict:
    system_prompt = (
    "You are a meeting scheduling assistant. Your job is to extract meeting details "
    "from a natural language request and respond in one of two ways:\n\n"
    "1. If all required details are present, respond with a valid JSON object having these exact keys:\n"
    "   - title: string\n"
    "   - date: string in YYYY-MM-DD format\n"
    "   - time: string in 24-hour format (HH:MM)\n"
    "   - duration: integer in minutes\n\n"
    "2. If any of these details are missing or unclear, respond with a friendly message asking the user "
    "for the missing information. Do NOT respond with an empty object or partial JSON.\n\n"
    "Only respond with either a complete JSON object or a clarification question."
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response.choices[0].message.content.strip()
    print("🧠 LLM raw output:", reply)

    try:
        parsed = json.loads(reply)
        return parsed  # Valid JSON: return directly
    except:
        # Not valid JSON, assume it's a follow-up question
        return {"follow_up": reply}
