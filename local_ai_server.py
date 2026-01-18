from fastapi import FastAPI
import subprocess
import os

app = FastAPI()
MODEL = "phi3:mini"

@app.get("/health")
def health():
    return {"status": "online", "model": MODEL}

@app.post("/analyze")
def analyze(payload: dict):
    prompt = payload.get("prompt", "")
    
    # Ensure UTF-8 encoding for input
    try:
        # Check if ollama is reachable
        # Use full path if needed, or assume PATH
        cmd = ["ollama", "run", MODEL, prompt]
        
        # Run subprocess with UTF-8 encoding
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=120  # Increased timeout for longer analysis
        )
        
        if result.returncode != 0:
            return {"error": f"Ollama Error: {result.stderr}"}
            
        return {"content": result.stdout}
        
    except FileNotFoundError:
        return {"error": "Ollama not found. Is it installed and in your PATH?"}
    except subprocess.TimeoutExpired:
        return {"error": "Analysis timed out (120s limit)."}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
