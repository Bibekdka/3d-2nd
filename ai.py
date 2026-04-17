import requests
import time
from config import (
    LOCAL_AI_URL, 
    LOCAL_AI_TIMEOUT, 
    LOCAL_AI_HEALTH_CHECK_TIMEOUT,
    REQUEST_MAX_RETRIES,
    REQUEST_RETRY_DELAY,
    get_logger
)

logger = get_logger("ai")

def _retry_request(func, *args, **kwargs):
    """Helper function to retry requests with exponential backoff."""
    last_exception = None
    
    for attempt in range(REQUEST_MAX_RETRIES):
        try:
            return func(*args, **kwargs)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            last_exception = e
            if attempt < REQUEST_MAX_RETRIES - 1:
                wait_time = REQUEST_RETRY_DELAY * (2 ** attempt)
                logger.warning(f"Request failed (attempt {attempt + 1}/{REQUEST_MAX_RETRIES}), retrying in {wait_time}s: {str(e)}")
                time.sleep(wait_time)
            else:
                logger.error(f"Request failed after {REQUEST_MAX_RETRIES} attempts: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in request: {str(e)}")
            raise
    
    if last_exception:
        raise last_exception

def ai_health_check():
    """Check health of AI server with retry logic."""
    try:
        def make_request():
            return requests.get(
                f"{LOCAL_AI_URL}/health",
                timeout=LOCAL_AI_HEALTH_CHECK_TIMEOUT
            )
        
        r = _retry_request(make_request)
        
        if r.status_code == 200:
            data = r.json()
            logger.info("AI server health check: OK")
            return {
                "status": "online",
                "model": data.get("model", "unknown"),
                "message": "Operational"
            }
        else:
            logger.warning(f"AI server returned HTTP {r.status_code}")
            return {
                "status": "error",
                "model": "unknown", 
                "message": f"HTTP {r.status_code}"
            }
    except requests.exceptions.ConnectionError as e:
        logger.warning(f"AI server connection refused: {str(e)}")
        return {
            "status": "offline",
            "model": "unknown",
            "message": "Connection Refused (Is server running?)"
        }
    except requests.exceptions.Timeout:
        logger.error(f"AI server health check timed out ({LOCAL_AI_HEALTH_CHECK_TIMEOUT}s)")
        return {
            "status": "offline",
            "model": "unknown",
            "message": "Health check timeout"
        }
    except Exception as e:
        logger.error(f"Unexpected error in health check: {str(e)}")
        return {
            "status": "error",
            "model": "unknown",
            "message": f"Error: {str(e)}"
        }

def ai_analyze(text: str):
    """Analyze text using AI server with retry logic."""
    try:
        if not text or not text.strip():
            logger.warning("ai_analyze called with empty text")
            return {
                "summary": "AI Error",
                "details": "Input text is empty"
            }
        
        def make_request():
            return requests.post(
                f"{LOCAL_AI_URL}/analyze",
                json={"prompt": text[:6000]},
                timeout=LOCAL_AI_TIMEOUT
            )
        
        r = _retry_request(make_request)
        data = r.json()
        
        logger.info(f"AI analysis completed successfully ({len(text)} chars input)")
        return {
            "summary": "Local AI",
            "details": data.get("content", "")
        }
    except requests.exceptions.Timeout:
        logger.error(f"AI analysis timed out ({LOCAL_AI_TIMEOUT}s)")
        return {
            "summary": "AI Error",
            "details": f"Analysis timed out (limit: {LOCAL_AI_TIMEOUT}s). Try a shorter input."
        }
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to AI server")
        return {
            "summary": "AI Error",
            "details": "Cannot connect to AI server. Is it running?"
        }
    except Exception as e:
        logger.error(f"AI analysis error: {str(e)}")
        return {
            "summary": "AI Error",
            "details": f"Error: {str(e)}"
        }

# --- Helpers required by app.py (preserved to prevent crashes) ---

def ai_generate_tags(text_summary: str) -> str:
    """Fallback stub for tags."""
    return "#3dprinting #scraped"

def ai_debug_connection():
    return [str(ai_health_check())]
