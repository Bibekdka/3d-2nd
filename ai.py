import requests

LOCAL_AI_URL = "http://127.0.0.1:8000"

def ai_health_check():
    try:
        r = requests.get(f"{LOCAL_AI_URL}/health", timeout=3)
        if r.status_code == 200:
            data = r.json()
            return {
                "status": "online",
                "model": data.get("model", "unknown")
            }
    except:
        pass

    return {
        "status": "offline",
        "message": "Ollama not running"
    }

def ai_analyze(text: str):
    try:
        # Increase timeout for local AI processing
        r = requests.post(
            f"{LOCAL_AI_URL}/analyze",
            json={"prompt": text[:6000]},
            timeout=120
        )
        data = r.json()
        
        if "error" in data:
             return {"summary": "AI Error", "details": data["error"]}
             
        return {
            "summary": "Local AI Analysis",
            "details": data.get("content", "")
        }
    except Exception as e:
        return {
            "summary": "AI Error",
            "details": str(e)
        }

def ai_generate_tags(text_summary: str) -> str:
    """Fallback stub for tags."""
    return "#3dprinting #scraped"

def ai_debug_connection():
    return [str(ai_health_check())]
