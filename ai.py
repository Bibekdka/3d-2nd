# ai.py - Stubs for AI functionality (currently on hold)

def ai_analyze(text: str) -> dict:
    """Fallback stub for AI analysis."""
    return {
        "summary": "AI Offline", 
        "details": "AI features are currently disabled.\n\n" + text[:500] + "..."
    }

def ai_generate_tags(text_summary: str) -> str:
    """Fallback stub for tags."""
    return "#3dprinting #scraped"

def ai_health_check():
    """Fallback stub for health check."""
    return {"status": "offline", "message": "AI Disabled (Code Cleanup)"}

def ai_debug_connection():
    return ["AI Disabled"]
