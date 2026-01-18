import os
import streamlit as st
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# CONFIGURATION
MODEL_PRIMARY = "gpt-4o-mini"
MODEL_FALLBACK = "gpt-4.1-mini"

# LOAD API KEY
if "OPENAI_API_KEY" in st.secrets:
    API_KEY = st.secrets["OPENAI_API_KEY"]
else:
    API_KEY = os.getenv("OPENAI_API_KEY")

def _get_client():
    if not OPENAI_AVAILABLE or not API_KEY:
        return None
    return OpenAI(api_key=API_KEY)

def _safe_completion(client, messages, max_tokens=None):
    """Attempts generation with primary model, falls back if needed."""
    try:
        return client.chat.completions.create(
            model=MODEL_PRIMARY,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7
        )
    except Exception as e1:
        print(f"⚠️ Primary Model Failed ({MODEL_PRIMARY}): {e1}")
        try:
            return client.chat.completions.create(
                model=MODEL_FALLBACK,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
        except Exception as e2:
            raise e2

def ai_analyze(text: str) -> dict:
    client = _get_client()
    if not client:
        return {"summary": "System Offline", "details": "OpenAI Library or Key Missing"}

    try:
        response = _safe_completion(
            client,
            messages=[
                {"role": "system", "content": "You are an expert 3D printing engineer. Analyze the following model data."},
                {"role": "user", "content": f"Analyze this 3D model text for printing risks, summary, and material recommendations: {text[:8000]}"}
            ]
        )
        result = response.choices[0].message.content
        return {"summary": "GPT Analysis", "details": result}
    except Exception as e:
        return {"summary": "Error", "details": f"GPT Error: {str(e)}"}

def ai_generate_tags(text_summary: str) -> str:
    client = _get_client()
    if not client: return "#manual"

    try:
        response = _safe_completion(
            client,
            messages=[
                {"role": "system", "content": "You are a tagging bot. Output only hashtags."},
                {"role": "user", "content": f"Generate 5 technical hashtags for this 3D print: {text_summary[:500]}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except:
        return "#3dprint #gpt"

def ai_health_check():
    """Checks if GPT is reachable."""
    if not OPENAI_AVAILABLE: return {"status": "offline", "message": "Library Missing"}
    if not API_KEY: return {"status": "offline", "message": "Key Missing"}

    try:
        client = _get_client()
        # Simple test generation
        _safe_completion(
            client,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1
        )
        return {"status": "online", "model": MODEL_PRIMARY}
    except Exception as e:
        err_msg = str(e)
        if "quota" in err_msg.lower():
            return {"status": "offline", "message": "No Credits (Check Billing)"}
        return {"status": "offline", "message": err_msg[:50]}

def ai_debug_connection():
    return [str(ai_health_check())]
