import google.generativeai as genai
import json
import re
import uuid

def generate_concept_map(text: str) -> dict:
    prompt = f"""
You are an AI assistant that extracts **concept maps** from **any textbook chapter**.

Your task is to return a valid **JSON object** in this exact format:

{{
  "concepts": [
    {{ "id": "cell_structure", "label": "Cell Structure" }},
    {{ "id": "cell_membrane", "label": "Cell Membrane" }}
  ],
  "relationships": [
    {{ "from": "cell_structure", "to": "cell_membrane", "type": "contains" }}
  ]
}}

### STRICT INSTRUCTIONS:
- Output **ONLY JSON**, no explanations, no markdown, no headings.
- Use **lowercase, underscore-separated** `id` values.
- Ensure `id` values are **unique**.
- `label` should be readable concept names taken from the text.
- Use relationship types: "causes", "depends_on", "part_of", "contains", "leads_to", etc.
- Do NOT invent concepts—use only real and important ones from the input.
- Structure must match the format exactly.

### Textbook Input:
{text.strip()}
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    # Extract JSON from raw response or inside ```json block
    match = re.search(r"```json\s*(.*?)```", response.text, re.DOTALL)
    json_str = match.group(1).strip() if match else response.text.strip()

    try:
        parsed = json.loads(json_str)

        # Fallback ID fix if format wasn’t followed
        for i, concept in enumerate(parsed.get("concepts", [])):
            if "id" not in concept or not re.match(r'^[a-z0-9_]+$', concept["id"]):
                concept["id"] = f"concept_{i}_{uuid.uuid4().hex[:4]}"
        return parsed

    except json.JSONDecodeError as e:
        print("❌ JSON parsing failed:", e)
        print("⚠️ Full response was:", response.text)
        return None
