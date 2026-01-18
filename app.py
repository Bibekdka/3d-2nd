import asyncio
import sys
import streamlit as st
import pandas as pd
import time
import os

# FIX WINDOWS ASYNC LOOP (Crucial for Playwright on Windows)
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# IMPORTS
from database import add_entry, load_history, update_print_status, get_learning_context, get_db_stats, check_connection
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

def main():
    st.set_page_config(page_title="3D Business Brain", page_icon="🧠", layout="wide")
    
    if "printers" not in st.session_state: 
        st.session_state["printers"] = PRINTER_PROFILES.copy()

    # --- SIDEBAR: The Brain Center & Global Config ---
    with st.sidebar:
        st.title("🧠 3D Business Brain")
        
        # 1. System Health
        if check_connection():
            st.success("🟢 Memory (Google Sheets): Online")
        else:
            st.error("🔴 Memory Offline (Check Secrets)")
            
        # 2. Printer & Tech Settings
        st.divider()
        st.subheader("🖨️ Tech Specs")
        printer_name = st.selectbox("Printer Profile", list(st.session_state["printers"].keys()))
        current_printer = st.session_state["printers"][printer_name]
        
        mat_type = st.selectbox("Material", list(MATERIAL_DENSITIES.keys()))
        density = MATERIAL_DENSITIES[mat_type]
        
        c1, c2 = st.columns(2)
        infill = c1.slider("Infill %", 10, 100, 20)
        walls = c2.slider("Walls %", 5, 100, 20)

        # 3. Business Logic (Feature 2 Requirements)
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

    # --- TAB 1: WEB SCOUT (Feature 1: Scraping + AI) ---
    with tab_scrape:
        st.header("🕵️ Model Intelligence Scout")
        url = st.text_input("Paste Model URL (MakerWorld, Printables, Thingiverse)")
        
        if st.button("🚀 Analyze Link", type="primary"):
            # A. Retrieve Context from Memory
            memory_context = get_learning_context()
            
            with st.status("Deploying Agents...", expanded=True) as status:
                # B. Scrape
                def update_ui(msg): st.write(f"_{msg}_")
                data = scrape_model_page(url, status_callback=update_ui)
                
                if "error" in data:
                    status.update(label="❌ Extraction Failed", state="error")
                    st.error(data["error"])
                    st.stop()
                
                # C. AI Analysis
                st.write("🧠 Analyzing design geometry & comments...")
                prompt = f"""
                Act as a 3D Printing Expert. 
                CONTEXT (Past Failures): {memory_context}
                MODEL DATA: {data['text']}
                
                OUTPUT FORMAT:
                1. **Verdict**: (Safe to Print / Risky / Do Not Print)
                2. **Summary**: What is this model?
                3. **Risks**: Potential failure points (overhangs, adhesion, tolerances).
                4. **Recommendation**: Settings advice (Material, Support, Orientation).
                """
                res = ai_analyze(prompt)
                tags = ai_generate_tags(res['details'])
                
                # Store in Session for "Save" button
                st.session_state['last_scan'] = {
                    "url": url,
                    "summary": res['summary'],
                    "details": res['details'],
                    "tags": tags,
                    "images": data.get("images", [])
                }
                
                status.update(label="✅ Analysis Complete", state="complete", expanded=False)

        # Result Display Area
        if 'last_scan' in st.session_state:
            scan = st.session_state['last_scan']
            
            # Show Images Gallery
            if scan['images']:
                st.image(scan['images'][:3], width=200, caption=["Img 1", "Img 2", "Img 3"])
            
            st.markdown("### 📝 AI Report")
            st.markdown(scan['details'])
            st.info(f"Generated Tags: {scan['tags']}")
            
            if st.button("💾 Save to Brain (History)"):
                if add_entry("Web Scrape", scan['url'], scan['details'], 0, scan['summary'], scan['tags']):
                    st.success("Saved to Database!")
                else:
                    st.error("Database Error.")

    # --- TAB 2: BUSINESS CALCULATOR (Feature 2: Dynamic Pricing) ---
    with tab_local:
        st.header("💼 Quote Generator")
        
        uploaded_files = st.file_uploader("Upload STL Files", type=["stl"], accept_multiple_files=True)
        
        if uploaded_files:
            total_invoice_value = 0
            
            st.markdown("### 🧾 Itemized Breakdown")
            
            for stl in uploaded_files:
                stl.seek(0)
                # 1. Physical Analysis
                stats = analyze_single_file_content(
                    stl.read(), stl.name, density, cost_kg, infill, walls,
                    current_printer['speed'], current_printer['nozzle']
                )
                
                if "error" in stats:
                    st.error(f"Error reading {stl.name}: {stats['error']}")
                    continue

                # 2. Business Math (The Logic you asked for)
                print_time_hours = stats['Print Time (hr)']
                material_cost = stats['Cost (₹)']
                weight_g = stats['Weight (g)']
                
                # Electricity: (Watts / 1000) * Hours * Rate
                power_consumption_kwh = (current_printer['watts'] / 1000) * print_time_hours
                electricity_cost = power_consumption_kwh * electricity_rate
                
                # Labor: Hours * Rate
                labor_cost = print_time_hours * labor_rate
                
                # Base Cost
                base_cost = material_cost + electricity_cost + labor_cost
                
                # Profit
                profit_amount = base_cost * (profit_margin / 100)
                
                # Total before Tax
                selling_price = base_cost + profit_amount
                
                total_invoice_value += selling_price

                # 3. Display Row
                with st.expander(f"📄 {stl.name} - Est: ₹{round(selling_price, 2)}", expanded=True):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Weight", f"{weight_g}g")
                    c2.metric("Time", f"{print_time_hours}h")
                    c3.metric("Material Cost", f"₹{material_cost}")
                    c4.metric("Elec + Labor", f"₹{round(electricity_cost + labor_cost, 2)}")
                    
                    st.caption(f"Base Cost: ₹{round(base_cost, 2)} | Profit: ₹{round(profit_amount, 2)}")

            st.divider()
            
            # 4. Final Invoice
            gst_amount = total_invoice_value * (gst_percent / 100)
            final_total = total_invoice_value + gst_amount + delivery_fee
            
            st.markdown("## 💰 Final Quote")
            
            i1, i2, i3, i4 = st.columns(4)
            i1.metric("Subtotal (Items)", f"₹{round(total_invoice_value, 2)}")
            i2.metric(f"GST ({gst_percent}%)", f"₹{round(gst_amount, 2)}")
            i3.metric("Delivery", f"₹{delivery_fee}")
            i4.metric("GRAND TOTAL", f"₹{round(final_total, 2)}", delta="Profit Included")

    # --- TAB 3: MEMORY BANK (Feature 4: History) ---
    with tab_history:
        st.header("📚 Printing History")
        
        # Stats
        stats = get_db_stats()
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Memories", stats['total'])
        c2.metric("Success Rate", f"{stats['success_rate']}%")
        
        st.divider()
        
        # Load Data
        df = load_history()
        if not df.empty:
            # Search
            search = st.text_input("🔍 Search History", placeholder="Enter filename, tag, or link...")
            if search:
                df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

            st.dataframe(
                df, 
                column_config={
                    "link": st.column_config.LinkColumn("Model Link"),
                    "details": "AI Notes",
                    "cost_inr": st.column_config.NumberColumn("Cost", format="₹%.2f")
                },
                use_container_width=True
            )
        else:
            st.info("No history found. Start analyzing models!")

if __name__ == "__main__":
    main()
