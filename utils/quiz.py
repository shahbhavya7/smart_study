import google.generativeai as genai
import json
import re

def generate_structured_quiz(text: str, num_questions=5) -> list:
    prompt = f"""
Generate a quiz from the following text in valid JSON format.
You are an AI that returns only valid JSON. Do not explain or include anything outside JSON.
Use this structure:

[
  {{
    "type": "mcq",
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "B"
  }},
  {{
    "type": "fill_blank",
    "question": "...",
    "answer": "..."
  }},
  {{
    "type": "true_false",
    "question": "...",
    "answer": "True"
  }}
]

Text:
{text.strip()}
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    # ✅ Extract JSON even if wrapped in triple backticks
    match = re.search(r"```json\s*(.*?)```", response.text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        json_str = response.text  # fallback if no code block

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("❌ JSON parsing failed:", e)
        print("⚠️ Full response was:", response.text)
        return None
