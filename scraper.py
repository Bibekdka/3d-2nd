import time
import os
import sys
import subprocess
from playwright.sync_api import sync_playwright

# Check safe mode
SAFE_MODE = os.getenv("STREAMLIT_SAFE_MODE", "false").lower() == "true"

def install_playwright_if_needed():
    """Install Playwright browser on cloud environments."""
    if sys.platform != "win32":
        try:
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        except:
            pass

def scrape_model_page(url, status_callback=None):
    """
    Robust scraper: Launches fresh browser per request to prevent Threading Errors.
    """
    if SAFE_MODE: return {"error": "Scraper disabled in production safe mode"}
    
    logs = []
    def report(msg):
        logs.append(msg)
        if status_callback: status_callback(msg)
        print(f"[Scraper] {msg}")

    IS_CLOUD = sys.platform != "win32"
    if IS_CLOUD: install_playwright_if_needed()

    try:
        report("🚀 Launching secure browser...")
        
        # NO CACHE HERE - Critical for Render stability
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"]
            )
            
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            report(f"🌐 Navigating to {url}...")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(1000)
            except Exception as e:
                report(f"⚠️ Navigation warning: {e}")

            # Scroll to bottom to trigger lazy loading
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, 0)") # Scroll back up
            page.wait_for_timeout(1000)

            # Click standard gallery expansion buttons if they exist
            try:
                page.get_by_role("button", name="Show all").click(timeout=1000)
            except: pass

            text = page.inner_text("body")
            
            # Filter for useful images with broader acceptance but strict exclusion
            images = page.eval_on_selector_all("img", """
                imgs => imgs.filter(i => 
                    i.src.startsWith('http') && 
                    !i.src.includes('avatar') && 
                    !i.src.includes('icon') &&
                    !i.src.includes('logo') &&
                    !i.src.includes('svg') &&
                    (i.naturalWidth > 200 || i.naturalHeight > 200)
                ).map(i => i.src)
            """)
            
            browser.close()
            
            # Limit text size for AI processing
            cleaned_text = "\n".join([l.strip() for l in text.splitlines() if len(l.strip()) > 30][:50000])
            
            report("✅ Extraction complete.")
            return {
                "text": cleaned_text,
                "images": list(set(images))[:500],
                "debug": logs
            }

    except Exception as e:
        return {"error": str(e), "debug": logs}
