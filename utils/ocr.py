import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_image_with_gemini(image_file):
    try:
        image_bytes = image_file.getvalue()  # Not .read()
        mime_type = image_file.type

        # Optionally validate the image
        Image.open(BytesIO(image_bytes)).verify()

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content([
            "Extract clean, readable text from this textbook image. Ignore noise, background, and markings.",
            {
                "mime_type": mime_type,
                "data": image_bytes
            }
        ])

        return response.text.strip()

    except Exception as e:
        return f"❌ Failed to process image: {str(e)}"
