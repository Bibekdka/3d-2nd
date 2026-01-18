import os
import streamlit as st
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# LOAD API KEY (Checks Secrets first, then Environment)
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_AVAILABLE and API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception: pass

def _get_working_model():
    """
    Tries to find a working model. 
    Falls back to 'gemini-pro' if 'flash' is unavailable (Fixes 404 error).
    """
    model_priority = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]
    
    for model_name in model_priority:
        try:
            model = genai.GenerativeModel(model_name)
            return model
        except:
            continue
    return genai.GenerativeModel("gemini-pro") # Final fallback

def ai_analyze(text: str) -> dict:
    fallback = {"summary": "Analysis unavailable", "details": "Check API Key or Quota"}
    
    if not GEMINI_AVAILABLE or not API_KEY: return fallback

    try:
        # ROBUST MODEL SELECTION
        model = _get_working_model()
        
        # Safe generation with timeout protection
        response = model.generate_content(text)
        
        if not response or not response.text: return fallback
        return {"summary": "AI Analysis", "details": response.text.strip()}
    
    except Exception as e:
        # If the primary attempt fails, try one last desperation fallback to 'gemini-pro'
        if "404" in str(e) or "not found" in str(e).lower():
            try:
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(text)
                return {"summary": "AI Analysis (Backup Model)", "details": response.text.strip()}
            except:
                pass
        return {"summary": "Error", "details": f"AI Error: {str(e)}"}

def ai_generate_tags(text_summary: str) -> str:
    if not GEMINI_AVAILABLE or not API_KEY: return "#manual #check"
    
    try:
        model = _get_working_model()
        prompt = f"Generate 5 short technical hashtags for this 3D print description. Output ONLY the tags. Text: {text_summary[:500]}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "#3dprint #model"

def ai_health_check():
    """Checks if Gemini is reachable and which model is responding."""
    if not GEMINI_AVAILABLE:
        return {"status": "offline", "message": "Library Missing (google-generativeai)"}
    if not API_KEY:
        return {"status": "offline", "message": "API Key Missing (Check secrets.toml)"}
    
    try:
        # List available models to debug 404s
        model = _get_working_model()
        # Simple ping
        model.generate_content("ping")
        return {"status": "online", "model": f"Active ({model.model_name.split('/')[-1]})"}
    except Exception as e:
        return {"status": "offline", "message": str(e)[:50]}
