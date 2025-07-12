import pdfplumber
from io import BytesIO

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()
