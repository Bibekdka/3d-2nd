import asyncio
import sys
import streamlit as st
import pandas as pd
import time
import os

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- IMPORTS ---
from database import add_entry, load_history, get_db_stats, check_connection, init_db
from scraper import scrape_model_page
from ai import ai_analyze, ai_generate_tags, ai_health_check, ai_debug_connection
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

    # Initialize DB
    init_db()

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🧠 3D Business Brain")
        
        if st.button("🚑 Quick Diagnosis"):
            ai_status = ai_health_check()
            if ai_status["status"] == "online": 
                st.success(f"AI: OK ({ai_status.get('model', 'Unknown')})")
            else: 
                st.error(f"AI: {ai_status['message']}")
                
        st.divider()
        st.subheader("🖨️ Tech Specs")
        printer_name = st.selectbox("Printer Profile", list(st.session_state["printers"].keys()))
        current_printer = st.session_state["printers"][printer_name]
        
        mat_type = st.selectbox("Material", list(MATERIAL_DENSITIES.keys()))
        density = MATERIAL_DENSITIES[mat_type]
        
        c1, c2 = st.columns(2)
        infill = c1.slider("Infill %", 10, 100, 20)
        walls = c2.slider("Walls %", 5, 100, 20)

        st.divider()
        st.subheader("💰 Business Economics")
        cost_kg = st.number_input("Filament Cost (₹/kg)", 500, 5000, 1200)
        electricity_rate = st.number_input("Electricity (₹/kWh)", 0.0, 50.0, 10.0)
        labor_rate = st.number_input("Labor Rate (₹/hr)", 0, 5000, 200)
        profit_margin = st.slider("Profit Margin (%)", 0, 300, 50)
        gst_percent = st.selectbox("GST (%)", [0, 5, 12, 18, 28], index=3)
        delivery_fee = st.number_input("Delivery Fee (₹)", 0, 2000, 100)

    # --- TABS ---
    tab_scrape, tab_local, tab_history, tab_db, tab_health = st.tabs(
        [
            "🌐 Forensic Scout",
            "💼 Business Calculator",
            "📚 Memory Bank",
            "🗄 Database Explorer",
            "🩺 Health"
        ]
    )

    # --- TAB 1: WEB SCOUT ---
    with tab_scrape:
        st.header("🕵️ Model Intelligence Scout")
        url = st.text_input("Paste Model URL")
        
        if st.button("🚀 Analyze Link", type="primary"):
            with st.status("Deploying Agents...", expanded=True) as status:
                def update_ui(msg): st.write(f"_{msg}_")
                data = scrape_model_page(url, status_callback=update_ui)
                
                if "error" in data:
                    status.update(label="❌ Extraction Failed", state="error")
                    st.error(data["error"])
                    st.stop()
                
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

        if 'last_scan' in st.session_state:
            scan = st.session_state['last_scan']
            if scan['images']:
                st.image(scan['images'][:3], width=200, caption=["Img 1", "Img 2", "Img 3"])
            
            st.markdown("### 📝 AI Report")
            st.markdown(scan['details'])
            st.info(f"Tags: {scan['tags']}")
            
            if st.button("💾 Save to Brain"):
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

            gst_amt = total_invoice * (gst_percent/100)
            grand_total = total_invoice + gst_amt + delivery_fee
            
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("Subtotal", f"₹{round(total_invoice, 2)}")
            c2.metric("GST", f"₹{round(gst_amt, 2)}")
            c3.metric("GRAND TOTAL", f"₹{round(grand_total, 2)}")
            
            if st.button("💾 Save Quote"):
                 if add_entry("Quote", "Batch", f"Total: {grand_total}", grand_total, "Quote", "#quote"):
                    st.success("Saved!")

    # --- TAB 3: HISTORY ---
    with tab_history:
        st.header("📚 History")
        df = load_history()
        if not df.empty: st.dataframe(df, use_container_width=True)
        else: st.info("No history yet.")

    # --- TAB 4: DATABASE EXPLORER ---
    with tab_db:
        st.header("🗄 Database Explorer")

        df = load_history()

        if df.empty:
            st.warning("Database is empty.")
            # We don't stop here so the rest of the UI still renders if needed, 
            # but user said 'st.stop()', so we follow instructions.
            st.stop()

        # --- Filters ---
        c1, c2, c3 = st.columns(3)

        with c1:
            # Handle potential missing 'type' column safely
            if 'type' in df.columns:
                type_options = ["All"] + sorted(df["type"].dropna().unique().tolist())
            else:
                type_options = ["All"]
            
            type_filter = st.selectbox(
                "Filter by Type",
                type_options
            )

        with c2:
            search = st.text_input("Search (URL, tags, details)")

        with c3:
            sort_by = st.selectbox(
                "Sort by",
                ["Newest", "Oldest", "Highest Amount", "Lowest Amount"]
            )

        # --- Apply Filters ---
        filtered_df = df.copy()

        if type_filter != "All":
            filtered_df = filtered_df[filtered_df["type"] == type_filter]

        if search:
            # Robust string conversion for search
            filtered_df = filtered_df[
                filtered_df.apply(
                    lambda row: search.lower() in str(row).lower(),
                    axis=1
                )
            ]

        # --- Sorting ---
        if sort_by == "Newest" and "created_at" in filtered_df.columns:
            filtered_df = filtered_df.sort_values("created_at", ascending=False)
        elif sort_by == "Oldest" and "created_at" in filtered_df.columns:
            filtered_df = filtered_df.sort_values("created_at", ascending=True)
        elif sort_by == "Highest Amount" and "amount" in filtered_df.columns:
            filtered_df = filtered_df.sort_values("amount", ascending=False)
        elif sort_by == "Lowest Amount" and "amount" in filtered_df.columns:
            filtered_df = filtered_df.sort_values("amount", ascending=True)

        # --- Display ---
        st.dataframe(filtered_df, use_container_width=True)

        # --- Export ---
        st.download_button(
            "⬇️ Download CSV",
            filtered_df.to_csv(index=False),
            file_name="database_export.csv",
            mime="text/csv"
        )

    # --- TAB 4: HEALTH DASHBOARD ---
    with tab_health:
        st.subheader("🩺 System Health")
        col1, col2 = st.columns(2)

        # DB Check
        with col1:
            st.markdown("### 🗄 Database")
            if check_connection():
                st.success("Online")
            else:
                st.error("Offline")

        # AI Check
        with col2:
            st.markdown("### 🧠 AI Engine")
            ai = ai_health_check()
            if ai["status"] == "online":
                st.success(f"Online: {ai.get('model', 'Unknown')}")
            else:
                st.error(f"Offline: {ai.get('message', 'Unknown Error')}")
        
        st.divider()
        with st.expander("🛠️ Deep Debugger (Click if AI is failing)", expanded=False):
            if st.button("Run Connection Test"):
                logs = ai_debug_connection()
                for log in logs:
                    if "❌" in log: st.error(log)
                    elif "✅" in log: st.success(log)
                    else: st.info(log)

if __name__ == "__main__":
    main()
