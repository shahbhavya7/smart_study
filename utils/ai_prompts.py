import google.generativeai as genai

def split_into_chunks(text, max_words=200):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def summarize_chunks_with_gemini(text):
    chunks = split_into_chunks(text)
    model = genai.GenerativeModel("gemini-2.5-flash")

    final_summary = ""
    for i, chunk in enumerate(chunks):
        prompt = f"Summarize the following part of a textbook in simple terms:\n\n{chunk}\n\nSummary:"
        response = model.generate_content(prompt)
        final_summary += f"### Summary Part {i+1}:\n{response.text.strip()}\n\n"
    
    return final_summary.strip()
