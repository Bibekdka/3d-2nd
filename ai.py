import os
import streamlit as st
import time

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# LOAD API KEY
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_AVAILABLE and API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception: pass

def _get_working_model(debug_log=None):
    """
    Iterates through models and TESTS them. 
    Only returns a model that successfully generates a response.
    """
    # Priority list: Flash (Fast/Cheap) -> Pro (Reliable) -> 1.0 Pro (Legacy)
    candidates = [
        "gemini-1.5-flash", 
        "gemini-1.5-flash-latest", 
        "gemini-pro", 
        "gemini-1.0-pro"
    ]
    
    for model_name in candidates:
        try:
            if debug_log is not None: debug_log.append(f"Testing {model_name}...")
            
            model = genai.GenerativeModel(model_name)
            # CRITICAL: Force a network call to check if it really works
            response = model.generate_content("test", request_options={"timeout": 5})
            
            if response and response.text:
                if debug_log is not None: debug_log.append(f"✅ SUCCESS: {model_name}")
                return model
        except Exception as e:
            if debug_log is not None: debug_log.append(f"❌ FAILED {model_name}: {str(e)[:100]}")
            continue
            
    # If all fail, return a default wrapper that returns error messages
    return None

def ai_analyze(text: str) -> dict:
    if not GEMINI_AVAILABLE or not API_KEY: 
        return {"summary": "System Offline", "details": "Check API Key or Library"}

    try:
        model = _get_working_model()
        if not model:
            return {"summary": "AI Error", "details": "All Gemini models failed (404/Auth). Check Debug Tab."}
            
        response = model.generate_content(text)
        return {"summary": "AI Analysis", "details": response.text.strip()}
    except Exception as e:
        return {"summary": "Error", "details": f"AI Error: {str(e)}"}

def ai_generate_tags(text_summary: str) -> str:
    if not GEMINI_AVAILABLE or not API_KEY: return "#manual #check"
    try:
        model = _get_working_model()
        if not model: return "#error #offline"
        
        prompt = f"Generate 5 short technical hashtags. Output ONLY tags: {text_summary[:500]}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "#3dprint #model"

def ai_debug_connection():
    """Returns a log of what happened when trying to connect."""
    logs = []
    if not GEMINI_AVAILABLE:
        return ["❌ Library 'google-generativeai' not found."]
    if not API_KEY:
        return ["❌ API Key not found in secrets or env."]
    
    logs.append(f"🔑 API Key found (ends in ...{str(API_KEY)[-4:]})")
    _get_working_model(debug_log=logs)
    return logs

def ai_health_check():
    """Simple status check for the UI badge."""
    if not GEMINI_AVAILABLE: return {"status": "offline", "message": "Lib Missing"}
    if not API_KEY: return {"status": "offline", "message": "Key Missing"}
    
    model = _get_working_model()
    if model:
        name = model.model_name.split("/")[-1] if hasattr(model, "model_name") else "Active"
        return {"status": "online", "model": name}
    else:
        return {"status": "offline", "message": "All Models Failed"}
