import asyncio
import sys
import streamlit as st
import pandas as pd
import time
import os

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

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

    # Initialize DB (Safe init)
    init_db()

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🧠 3D Business Brain")
        
        # Quick Health Status
        ai_status = ai_health_check()
        db_status = check_connection()
        
        if ai_status["status"] == "online" and db_status["status"]:
            st.success("System: ONLINE")
        else:
            if not db_status["status"]: st.warning("DB: Offline")
            if ai_status["status"] != "online": st.warning(f"AI: {ai_status['status']}")
                
        st.divider()
        st.subheader("🤖 AI Control")

        if "ai_enabled" not in st.session_state:
            st.session_state["ai_enabled"] = False

        ai_toggle = st.toggle(
            "Enable Local AI (Ollama)",
            value=st.session_state["ai_enabled"]
        )

        st.session_state["ai_enabled"] = ai_toggle

        if ai_toggle:
            if ai_status["status"] == "online":
                st.success(f"Connected: {ai_status['model']}")
            else:
                st.error("AI Enabled but Offline")
                st.caption(ai_status["message"])
        else:
            st.info("AI Disabled")

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
    tab_intelli, tab_calc, tab_health = st.tabs(
        [
            "🧠 Intelli-DB",
            "💼 Quote Calculator",
            "🩺 System Health"
        ]
    )

    # --- TAB 1: INTELLI-DB (Merged Scraper + DB) ---
    with tab_intelli:
        # --- SECTION A: ADD INTELLIGENCE ---
        with st.expander("🕵️ Add New Intelligence (Scrape & Analyze)", expanded=True):
            st.caption("Paste a URL from MakerWorld, Printables, or Thingiverse to analyze and save.")
            
            c_url, c_btn = st.columns([4, 1])
            url = c_url.text_input("Model URL", placeholder="https://...")
            
            if c_btn.button("🚀 Analyze", type="primary"):
                if not url:
                    st.toast("Please enter a URL first.")
                else:
                    with st.status("Deploying Agents...", expanded=True) as status:
                        def update_ui(msg): st.write(f"_{msg}_")
                        data = scrape_model_page(url, status_callback=update_ui)
                        
                        if "error" in data:
                            status.update(label="❌ Extraction Failed", state="error")
                            st.error(data["error"])
                            # Don't stop, let them try again
                        else:
                            st.write("🧠 Reading geometry...")
                            prompt = f"Analyze this 3D model for printing risks, commercial viability, and optimal settings. Summary: {data['text'][:6000]}"
                            
                            # --- AI LOGIC ---
                            if st.session_state.get("ai_enabled"):
                                res = ai_analyze(prompt)
                            else:
                                res = {
                                    "summary": "AI Disabled",
                                    "details": "Enable AI in sidebar for full analysis.\n\nExtracted Text Sample:\n" + data['text'][:500] + "..."
                                }
                            
                            tags = ai_generate_tags(res['details'])
                            
                            # Store in session state for display/saving
                            st.session_state['last_scan'] = {
                                "url": url,
                                "summary": res['summary'],
                                "details": res['details'],
                                "tags": tags,
                                "images": data.get("images", [])
                            }
                            status.update(label="✅ Analysis Complete", state="complete", expanded=False)

            # Display Result & Save
            if 'last_scan' in st.session_state:
                scan = st.session_state['last_scan']
                st.divider()
                
                col_img, col_txt = st.columns([1, 2])
                with col_img:
                    if scan['images']:
                        st.image(scan['images'][0], caption="Primary Preview", use_container_width=True)
                        with st.expander("More Images"):
                            for img in scan['images'][1:4]:
                                st.image(img)
                
                with col_txt:
                    st.subheader("📝 Analysis Report")
                    st.markdown(scan['details'])
                    st.info(f"Tags: {scan['tags']}")
                    
                    if st.button("💾 Save to Knowledge Base"):
                        if not db_status["status"]:
                            st.error(f"Cannot save: {db_status['error']}")
                        else:
                            if add_entry("Web Scrape", scan['url'], scan['details'], 0, scan['summary'], scan['tags'], scan['images']):
                                st.success("✅ Saved to Database!")
                                time.sleep(1)
                                st.rerun() # Refresh to show in table below
                            else:
                                st.error("Database Error.")

        st.divider()
        
        # --- SECTION B: KNOWLEDGE BASE (DB View) ---
        st.subheader("📚 Knowledge Base")
        
        if not db_status["status"]:
            st.error(f"⚠️ Database Offline: {db_status['error']}")
            st.info("Check the Health tab for diagnosis.")
        else:
            df = load_history()
            if df.empty:
                st.info("Database is empty. Add some intelligence above!")
            else:
                # --- Filters ---
                c1, c2, c3 = st.columns(3)
                with c1:
                    if 'type' in df.columns:
                        type_options = ["All"] + sorted(df["type"].dropna().unique().tolist())
                    else: type_options = ["All"]
                    type_filter = st.selectbox("Filter by Type", type_options)
                with c2:
                    search = st.text_input("Search (URL, tags)")
                with c3:
                    sort_by = st.selectbox("Sort", ["Newest", "Oldest"])

                # --- Apply Filters ---
                filtered_df = df.copy()
                if type_filter != "All":
                    filtered_df = filtered_df[filtered_df["type"] == type_filter]
                if search:
                    filtered_df = filtered_df[filtered_df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
                
                if sort_by == "Newest" and "created_at" in filtered_df.columns:
                    filtered_df = filtered_df.sort_values("created_at", ascending=False)
                elif sort_by == "Oldest" and "created_at" in filtered_df.columns:
                    filtered_df = filtered_df.sort_values("created_at", ascending=True)

                # Format Date for Display
                if "created_at" in filtered_df.columns:
                     filtered_df["Date"] = pd.to_datetime(filtered_df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")
                     # Reorder columns to put Date first
                     cols = ["Date"] + [c for c in filtered_df.columns if c != "Date" and c != "created_at"]
                     filtered_df = filtered_df[cols]

                st.dataframe(filtered_df, use_container_width=True, hide_index=True)
                
                st.download_button("⬇️ Download CSV", filtered_df.to_csv(index=False), "brain_dump.csv", "text/csv")

    # --- TAB 2: QUOTE CALCULATOR ---
    with tab_calc:
        st.header("💼 Intelligent Quote Generator")
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
                    c_a, c_b = st.columns(2)
                    c_a.metric("Print Time", f"{round(p_time, 2)} hr")
                    c_b.metric("Material", f"{round(stats['Weight (g)'], 1)}g")
                    st.json(stats)

            gst_amt = total_invoice * (gst_percent/100)
            grand_total = total_invoice + gst_amt + delivery_fee
            
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("Subtotal", f"₹{round(total_invoice, 2)}")
            c2.metric(f"GST ({gst_percent}%)", f"₹{round(gst_amt, 2)}")
            c3.metric("GRAND TOTAL", f"₹{round(grand_total, 2)}")
            
            if st.button("💾 Save Quote to DB"):
                 if not db_status["status"]:
                     st.error("Cannot save: Database Offline")
                 else:
                     details_str = f"Files: {[f.name for f in uploaded_files]}, Subtotal: {total_invoice}"
                     if add_entry("Quote", "Batch File Upload", details_str, grand_total, "Customer Quote", "#quote"):
                        st.success("✅ Quote Saved!")

    # --- TAB 3: HEALTH DASHBOARD ---
    with tab_health:
        st.header("🩺 System Diagnostics")
        
        # 1. Database Check
        st.subheader("1. Database Connection")
        if db_status["status"]:
            st.success("✅ Google Sheets API: Connected")
            st.caption(f"Target Sheet: {SHEET_NAME}") # Placeholder, real check was inside
        else:
            st.error("❌ Google Sheets API: Disconnected")
            st.code(f"Error: {db_status['error']}")
            if "Missing" in str(db_status["error"]):
                st.info("💡 Action: Add your service account JSON to secrets.toml under [gsheets]")

        st.divider()

        # 2. AI Check
        st.subheader("2. AI Intelligence (Ollama)")
        col_ai_1, col_ai_2 = st.columns(2)
        with col_ai_1:
            st.metric("Status", ai_status["status"].upper(), 
                     delta="Online" if ai_status["status"] == "online" else "Offline",
                     delta_color="normal" if ai_status["status"] == "online" else "inverse")
        with col_ai_2:
            st.metric("Model", ai_status["model"])
            
        st.caption(f"Message: {ai_status['message']}")
        
        if ai_status["status"] != "online":
            st.warning("To fix: Run 'start_ai.bat' or ensure Ollama is serving.")
            if st.button("🛠️ Run Deep Connection Test"):
                logs = ai_debug_connection()
                st.write(logs)


if __name__ == "__main__":
    main()
