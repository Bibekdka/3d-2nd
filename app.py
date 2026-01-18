import asyncio
import sys
import streamlit as st
import pandas as pd
import time
import os

# FIX WINDOWS ASYNC LOOP (Crucial for Playwright on Windows)
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- CORRECTED IMPORTS ---
# We are importing from your actual flat files, not 'core.*'
from database import add_entry, load_history, get_db_stats, check_connection
from scraper import scrape_model_page
from ai import ai_analyze, ai_generate_tags
from app_utils import analyze_single_file_content 

# --- CONFIGURATION ---
PRINTER_PROFILES = {
    "Ender 3 / V2": {"speed": 50, "nozzle": 0.4, "watts": 350},
    "Bambu P1/X1": {"speed": 120, "nozzle": 0.4, "watts": 1000},
    "Prusa MK3/4": {"speed": 70, "nozzle": 0.4, "watts": 200}
}

MATERIAL_DENSITIES = {"PLA": 1.24, "PETG": 1.27, "ABS": 1.04, "TPU": 1.21}

def run_diagnosis():
    """Runs a live test on Brain (Sheets) and Eyes (Gemini)"""
    st.sidebar.markdown("### 🛠️ System Diagnostic")
    
    # 1. Test Database
    with st.sidebar.status("Testing Memory (Google Sheets)...") as status:
        if check_connection():
            status.update(label="✅ Memory Online", state="complete")
        else:
            status.update(label="❌ Memory Offline", state="error")
            st.sidebar.error("Check 'gcp_service_account' in secrets.")

    # 2. Test AI
    with st.sidebar.status("Testing AI (Gemini)...") as status:
        try:
            test_tag = ai_generate_tags("Test print")
            if "#" in test_tag or "manual" in test_tag:
                status.update(label="✅ AI Online", state="complete")
            else:
                status.update(label="⚠️ AI Unresponsive", state="error")
        except Exception as e:
            status.update(label=f"❌ AI Error: {e}", state="error")

def main():
    st.set_page_config(page_title="3D Business Brain", page_icon="🧠", layout="wide")
    
    if "printers" not in st.session_state: 
        st.session_state["printers"] = PRINTER_PROFILES.copy()

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🧠 3D Business Brain")
        
        # --- NEW DIAGNOSIS BUTTON ---
        if st.button("🚑 Run System Diagnosis"):
            run_diagnosis()
            
        st.divider()
        st.subheader("🖨️ Tech Specs")
        printer_name = st.selectbox("Printer Profile", list(st.session_state["printers"].keys()))
        current_printer = st.session_state["printers"][printer_name]
        
        mat_type = st.selectbox("Material", list(MATERIAL_DENSITIES.keys()))
        density = MATERIAL_DENSITIES[mat_type]
        
        c1, c2 = st.columns(2)
        infill = c1.slider("Infill %", 10, 100, 20)
        walls = c2.slider("Walls %", 5, 100, 20)

        # Business Logic
        st.divider()
        st.subheader("💰 Business Economics")
        cost_kg = st.number_input("Filament Cost (₹/kg)", 500, 5000, 1200)
        electricity_rate = st.number_input("Electricity (₹/kWh)", 0.0, 50.0, 10.0)
        labor_rate = st.number_input("Labor Rate (₹/hr)", 0, 5000, 200)
        profit_margin = st.slider("Profit Margin (%)", 0, 300, 50)
        gst_percent = st.selectbox("GST (%)", [0, 5, 12, 18, 28], index=3)
        delivery_fee = st.number_input("Delivery Fee (₹)", 0, 2000, 100)

    # --- TABS ---
    tab_scrape, tab_local, tab_history = st.tabs(["🌐 Forensic Scout", "💼 Business Calculator", "📚 Memory Bank"])

    # --- TAB 1: WEB SCOUT ---
    with tab_scrape:
        st.header("🕵️ Model Intelligence Scout")
        url = st.text_input("Paste Model URL")
        
        if st.button("🚀 Analyze Link", type="primary"):
            with st.status("Deploying Agents...", expanded=True) as status:
                # Scrape
                def update_ui(msg): st.write(f"_{msg}_")
                data = scrape_model_page(url, status_callback=update_ui)
                
                if "error" in data:
                    status.update(label="❌ Extraction Failed", state="error")
                    st.error(data["error"])
                    st.stop()
                
                # AI Analysis
                st.write("🧠 Analyzing design geometry...")
                prompt = f"Analyze this 3D model for printing risks and summary: {data['text'][:5000]}"
                res = ai_analyze(prompt)
                tags = ai_generate_tags(res['details'])
                
                st.session_state['last_scan'] = {
                    "url": url,
                    "summary": res['summary'],
                    "details": res['details'],
                    "tags": tags,
                    "images": data.get("images", [])
                }
                status.update(label="✅ Analysis Complete", state="complete", expanded=False)

        # Display Results
        if 'last_scan' in st.session_state:
            scan = st.session_state['last_scan']
            if scan['images']:
                st.image(scan['images'][:3], width=200, caption=["Img 1", "Img 2", "Img 3"])
            
            st.markdown("### 📝 AI Report")
            st.markdown(scan['details'])
            st.info(f"Tags: {scan['tags']}")
            
            if st.button("💾 Save to Brain"):
                # MAP 'save_history' TO 'add_entry'
                if add_entry("Web Scrape", scan['url'], scan['details'], 0, scan['summary'], scan['tags']):
                    st.success("Saved!")
                else:
                    st.error("Database Error.")

    # --- TAB 2: BUSINESS CALCULATOR ---
    with tab_local:
        st.header("💼 Quote Generator")
        uploaded_files = st.file_uploader("Upload STL Files", type=["stl"], accept_multiple_files=True)
        
        if uploaded_files:
            total_invoice = 0
            for stl in uploaded_files:
                stl.seek(0)
                stats = analyze_single_file_content(
                    stl.read(), stl.name, density, cost_kg, infill, walls,
                    current_printer['speed'], current_printer['nozzle']
                )
                
                if "error" in stats:
                    st.error(f"Error {stl.name}: {stats['error']}")
                    continue

                # Cost Calculation
                p_time = stats['Print Time (hr)']
                mat_cost = stats['Cost (₹)']
                
                elec_cost = (current_printer['watts']/1000) * p_time * electricity_rate
                labor_cost = p_time * labor_rate
                base_cost = mat_cost + elec_cost + labor_cost
                profit_amt = base_cost * (profit_margin/100)
                final_item_price = base_cost + profit_amt
                
                total_invoice += final_item_price

                with st.expander(f"{stl.name} - ₹{round(final_item_price, 2)}"):
                    st.json(stats)
                    st.write(f"Base Cost: ₹{round(base_cost, 2)} (Mat: {mat_cost} + Elec: {round(elec_cost,2)} + Labor: {labor_cost})")

            # Final Totals
            gst_amt = total_invoice * (gst_percent/100)
            grand_total = total_invoice + gst_amt + delivery_fee
            
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("Subtotal", f"₹{round(total_invoice, 2)}")
            c2.metric("GST", f"₹{round(gst_amt, 2)}")
            c3.metric("GRAND TOTAL", f"₹{round(grand_total, 2)}")

            if st.button("💾 Save Quote to History"):
                details_str = f"Quote for {len(uploaded_files)} files. Total: {grand_total}"
                if add_entry("Quote", "Batch Upload", details_str, grand_total, "Business Calculation", "#quote #order"):
                    st.success("Quote Saved!")

    # --- TAB 3: HISTORY ---
    with tab_history:
        st.header("📚 History")
        stats = get_db_stats()
        st.write(f"**Total Memories:** {stats['total']} | **Success Rate:** {stats['success_rate']}%")
        
        df = load_history()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No history yet.")

if __name__ == "__main__":
    main()
