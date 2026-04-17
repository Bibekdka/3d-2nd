from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import logging
import sys
from config import get_logger, is_production

logger = get_logger("ai_server")

app = FastAPI(title="3D Brain AI Server", version="1.0.0")
MODEL = os.getenv("AI_MODEL", "phi3:mini")

# Request/Response models
class AnalysisRequest(BaseModel):
    prompt: str
    max_length: int = 6000

class HealthResponse(BaseModel):
    status: str
    model: str
    message: str

@app.get("/health", response_model=HealthResponse)
def health():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {
        "status": "online",
        "model": MODEL,
        "message": "Operational"
    }

@app.post("/analyze")
def analyze(payload: AnalysisRequest):
    """Analyze prompt using Ollama model."""
    try:
        prompt = payload.prompt
        max_length = payload.max_length
        
        if not prompt or not prompt.strip():
            logger.warning("Empty prompt received")
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        # Truncate prompt if too long
        if len(prompt) > max_length:
            logger.info(f"Prompt truncated from {len(prompt)} to {max_length} chars")
            prompt = prompt[:max_length]
        
        logger.info(f"Starting analysis with model '{MODEL}' (input: {len(prompt)} chars)")
        
        # Check if Ollama is available
        try:
            cmd = ["ollama", "run", MODEL, prompt]
            
            # Run subprocess with UTF-8 encoding and timeout
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=120
            )
            
            if result.returncode != 0:
                error_msg = f"Ollama returned error code {result.returncode}: {result.stderr}"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)
            
            logger.info(f"Analysis completed successfully ({len(result.stdout)} chars output)")
            return {"content": result.stdout.strip()}
            
        except FileNotFoundError:
            error_msg = "Ollama not found. Is it installed and in your PATH?"
            logger.error(error_msg)
            raise HTTPException(status_code=503, detail=error_msg)
        except subprocess.TimeoutExpired:
            error_msg = "Analysis timed out (120s limit)"
            logger.error(error_msg)
            raise HTTPException(status_code=504, detail=error_msg)
            
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Unexpected error during analysis: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": "3D Brain AI Server",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting AI server with model '{MODEL}'")
    logger.info(f"Production mode: {is_production()}")
    
    # Determine host based on environment
    host = "0.0.0.0" if is_production() else "127.0.0.1"
    port = int(os.getenv("AI_SERVER_PORT", "8000"))
    
    logger.info(f"Listening on {host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info" if not is_production() else "warning"
    )
