import requests

LOCAL_AI_URL = "http://127.0.0.1:8000"

def ai_health_check():
    try:
        r = requests.get(f"{LOCAL_AI_URL}/health", timeout=2)
        if r.status_code == 200:
            data = r.json()
            return {
                "status": "online",
                "model": data.get("model", "unknown"),
                "message": "Operational"
            }
        else:
            return {
                "status": "error",
                "model": "unknown", 
                "message": f"HTTP {r.status_code}"
            }
    except requests.exceptions.ConnectionError:
        return {
            "status": "offline",
            "model": "unknown",
            "message": "Connection Refused (Is server running?)"
        }
    except Exception as e:
        return {
            "status": "error",
            "model": "unknown",
            "message": str(e)
        }

def ai_analyze(text: str):
    try:
        r = requests.post(
            f"{LOCAL_AI_URL}/analyze",
            json={"prompt": text[:6000]},
            timeout=60
        )
        data = r.json()
        return {
            "summary": "Local AI",
            "details": data.get("content", "")
        }
    except Exception as e:
        return {
            "summary": "AI Error",
            "details": str(e)
        }

# --- Helpers required by app.py (preserved to prevent crashes) ---

def ai_generate_tags(text_summary: str) -> str:
    """Fallback stub for tags."""
    return "#3dprinting #scraped"

def ai_debug_connection():
    return [str(ai_health_check())]
