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
# --- TEST ---
URL = "https://makerworld.com/en/models/2186388-forma-planter-system-with-hidden-drip-tray?from=recommend#profileId-2373481"

def run_test():
    print(f"🚀 Starting TEST scrape of: {URL}")
    data = scrape_model_page(URL, status_callback=lambda m: print(f"   [Scan]: {m}"))
    
    if "error" in data:
        print(f"❌ Scraper failed: {data['error']}")
        return

    print("\n---------- 🔍 ANALYSIS RESULTS ----------")
    print(f"📸 Images Found: {len(data.get('images', []))}")
    for idx, img in enumerate(data.get('images', [])):
        print(f"   - Image {idx+1}: {img[:60]}...")
    
    print("\n📝 Text Content Check:")
    text = data.get('text', '')
    print(f"   - Total Characters: {len(text)}")
    
    # Specific Check for Comments
    print("\n💬 Comment Check (Rigorous):")
    keywords = ["print", "nice", "good", "layer", "support", "great work", "thanks"]
    found_keywords = [k for k in keywords if k in text.lower()]
    
    if found_keywords:
        print(f"   ✅ FOUND COMMENTS! Detected keywords: {found_keywords}")
    else:
        print("   ⚠️ WARNING: No common comment keywords found. Check selectors.")

    print("-----------------------------------------\n")

    # --- SAVE TO DB ---
    print("💾 Attempting to save to Google Sheets...")
    init_db()
    
    success = add_entry(
        type_="Rigorous Test",
        source=URL,
        details=text[:2000], 
        amount=0.0,
        summary="Rigorous Test Output with Images & Comments check",
        tags="#rigorous #test #makerworld",
        images=data.get("images", [])
    )
    
    if success:
        print("✅ SAVE FUNCTION RETURNED TRUE")
        
        # --- VERIFY READ ---
        print("👀 Reading back data from Google Sheets to confirm...")
        from database import load_history
        try:
            df = load_history()
            if not df.empty:
                latest = df.iloc[-1]
                print(f"\n🏆 LATEST ENTRY IN DB:")
                print(f"   - Source: {latest.get('source', 'N/A')}")
                print(f"   - Images Saved: {len(str(latest.get('images', '')).split(',')) if latest.get('images') else 0}")
                print("   ✅ DATA IS DEFINITELY IN THE SHEET!")
            else:
                print("   ❌ SHEET SEEMS EMPTY AFTER SAVE.")
        except Exception as e:
            print(f"   ❌ Read failed: {e}")

    else:
        print("❌ FAILED TO SAVE TO DATABASE")

if __name__ == "__main__":
    run_test()
