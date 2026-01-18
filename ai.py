import os
import streamlit as st
import requests

GROK_API_KEY = os.getenv("GROK_API_KEY")
AI_PROVIDER = os.getenv("AI_PROVIDER", "grok")

GROK_API_URL = "https://api.x.ai/v1/chat/completions"

# -------------------------------
# GROK AI CALL
# -------------------------------
def grok_analyze(text: str) -> dict:
    if not GROK_API_KEY:
        return {"summary": "Offline", "details": "Grok API key missing"}

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-2-mini",
        "messages": [
            {"role": "system", "content": "You are an expert 3D printing engineer."},
            {"role": "user", "content": text[:6000]}
        ],
        "temperature": 0.6
    }

    try:
        r = requests.post(GROK_API_URL, headers=headers, json=payload, timeout=20)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
        return {"summary": "Grok Analysis", "details": content}
    except Exception as e:
        return {"summary": "Error", "details": str(e)}

# -------------------------------
# AI HEALTH CHECK (USED BY UI)
# -------------------------------
def ai_health_check():
    if AI_PROVIDER != "grok":
        return {"status": "offline", "message": "AI_PROVIDER not set to grok"}

    if not GROK_API_KEY:
        return {"status": "offline", "message": "Grok API key missing"}

    try:
        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "grok-2-mini",
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 1
        }

        r = requests.post(GROK_API_URL, headers=headers, json=payload, timeout=10)
        r.raise_for_status()
        return {"status": "online", "model": "Grok-2-mini"}

    except Exception as e:
        return {"status": "offline", "message": str(e)}

# -------------------------------
# MAIN AI ENTRY POINT
# -------------------------------
def ai_analyze(text: str) -> dict:
    return grok_analyze(text)

# Added to support existing calls in app.py
def ai_generate_tags(text_summary: str) -> str:
    # Minimal implementation using Grok if needed, or fallback
    return "#grok #3dprinting" 

# Added to support existing calls in app.py
def ai_debug_connection():
    return [str(ai_health_check())]
