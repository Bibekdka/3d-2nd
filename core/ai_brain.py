import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

def ai_notes(text: str) -> dict:
    if not API_KEY:
        return {
            "Error": "Gemini API key not configured",
            "Fallback": "Add GEMINI_API_KEY to environment"
        }

    prompt = f"""
You are a senior 3D printing expert.

Analyze the following model description and give:
1. What to do
2. What not to do
3. Print risks
4. Alternate design suggestions

Text:
{text[:3000]}
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return {
        "AI Analysis": response.text.strip()
    }
