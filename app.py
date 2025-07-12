import streamlit as st
from utils.pdf_parser import extract_text_from_pdf
from utils.ocr import extract_text_from_image_with_gemini
from utils.ai_prompts import summarize_chunks_with_gemini
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
# Configure the Gemini API key
if "GEMINI_API_KEY" in os.environ:
    # Ensure this is configured once in app.py or globally
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Streamlit app configuration

st.set_page_config(page_title="Smart Textbook Buddy", layout="centered")
st.title("📚 Smart Textbook Companion")

uploaded_file = st.file_uploader("Upload a textbook image or PDF", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        st.success("PDF uploaded successfully!")
        raw_text = extract_text_from_pdf(uploaded_file)
    elif file_type.startswith("image/"):
        st.success("Image uploaded successfully!")
        st.image(Image.open(uploaded_file), caption="Uploaded Image", use_container_width=True)
        raw_text = extract_text_from_image_with_gemini(uploaded_file)
    else:
        st.error("Unsupported file type.")
        raw_text = ""

    if raw_text:
        st.subheader("📄 Extracted Text")
        st.text_area("Raw Text", raw_text, height=300)

        if st.button("🧠 Summarize with Gemini"):
            with st.spinner("Generating summary..."):
                summary = summarize_chunks_with_gemini(raw_text)
                st.subheader("📝 Chapter Summary")
                st.markdown(summary, unsafe_allow_html=True)
