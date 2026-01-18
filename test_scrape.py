import os
import sys
import toml
import streamlit as st
from unittest.mock import MagicMock

# --- MOCK STREAMLIT SECRETS ---
# We need to load secrets manually since we aren't running via 'streamlit run'
try:
    with open(".streamlit/secrets.toml", "r") as f:
        secrets_data = toml.load(f)
    
    # Mock st.secrets
    # Streamlit secrets behaves like a dict but also an object, 
    # but for simple dict access this patch might be enough if code uses st.secrets["key"]
    st.secrets = secrets_data
    print("✅ Secrets loaded and mocked for testing.")
except Exception as e:
    print(f"❌ Failed to load secrets: {e}")
    sys.exit(1)

# --- IMPORTS AFTER MOCKING ---
from scraper import scrape_model_page
from database import add_entry, init_db

# --- TEST ---
URL = "https://makerworld.com/en/models/2186388-forma-planter-system-with-hidden-drip-tray?from=recommend#profileId-2373481"

def run_test():
    print(f"🚀 Starting scrape of: {URL}")
    data = scrape_model_page(URL)
    
    if "error" in data:
        print(f"❌ Scraper failed: {data['error']}")
        return

    print("\n---------- SCRAPED DATA ----------")
    print(f"Images Found: {len(data.get('images', []))}")
    print(f"Text Length: {len(data.get('text', ''))} chars")
    print(f"Snippet: {data.get('text', '')[:500]}...")
    print("----------------------------------\n")

    # --- SAVE TO DB ---
    print("💾 Attempting to save to Google Sheets...")
    
    # Ensure DB is init (creates sheet if needed)
    init_db()
    
    success = add_entry(
        type_="Test Scrape",
        source=URL,
        details=data.get("text", "")[:1000], # Save first 1000 chars as details
        amount=0.0,
        summary="Test Run Output with Images",
        tags="#test #makerworld #images",
        images=data.get("images", [])
    )
    
    if success:
        print("✅ SUCCESSFULLY SAVED TO GOOGLE SHEETS")
    else:
        print("❌ FAILED TO SAVE TO DATABASE")

if __name__ == "__main__":
    run_test()
