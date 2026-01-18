import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials

# --- CONFIGURATION ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
SHEET_NAME = "printer_brain"
WORKSHEET_NAME = "history"

# --- AUTHENTICATION ---
def get_gspread_client():
    """
    Authenticate using Streamlit Secrets.
    Expected secret structure:
    [gsheets]
    type = "service_account"
    project_id = "..."
    ...
    """
    if "gsheets" not in st.secrets:
        st.error("❌ Missing '[gsheets]' section in secrets.toml")
        return None

    creds_dict = dict(st.secrets["gsheets"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

# --- CORE FUNCTIONS ---
def check_connection():
    """Checks if we can access the Google Sheet."""
    try:
        client = get_gspread_client()
        if not client: return False
        
        # Try to open the sheet
        client.open(SHEET_NAME)
        return True
    except Exception as e:
        print(f"DB CONNECTION ERROR: {e}")
        return False

def init_db():
    """
    Ensures the target Sheet and Worksheet exist with correct headers.
    """
    try:
        client = get_gspread_client()
        if not client: return

        try:
            sh = client.open(SHEET_NAME)
        except gspread.SpreadsheetNotFound:
            # Note: Service accounts often can't create sheets in your personal Drive 
            # without being shared a folder. Better to ask user to create it.
            st.error(f"❌ Google Sheet '{SHEET_NAME}' not found. Please create it and share with the service account email.")
            return

        try:
            wks = sh.worksheet(WORKSHEET_NAME)
        except gspread.WorksheetNotFound:
            wks = sh.add_worksheet(title=WORKSHEET_NAME, rows=100, cols=10)
            # Create Headers
            wks.append_row(["type", "source", "details", "amount", "summary", "tags", "images", "created_at"])
            
    except Exception as e:
        st.error(f"DB INIT ERROR: {e}")

def add_entry(type_, source, details, amount, summary, tags, images=None):
    """
    Appends a new row to the history worksheet.
    """
    try:
        client = get_gspread_client()
        if not client: return False

        sh = client.open(SHEET_NAME)
        wks = sh.worksheet(WORKSHEET_NAME)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Handle optional images
        if images is None: images = []
        # Convert list to string if needed, or leave as string
        images_str = str(images) if isinstance(images, list) else str(images)
        
        # Append row
        wks.append_row([type_, source, details, amount, summary, tags, images_str, timestamp])
        return True
    except Exception as e:
        print(f"ADD ENTRY ERROR: {e}")
        st.error(f"Failed to save: {e}")
        return False

def load_history():
    """
    Fetches all records from the sheet and returns a pandas DataFrame.
    """
    try:
        client = get_gspread_client()
        if not client: return pd.DataFrame()

        sh = client.open(SHEET_NAME)
        wks = sh.worksheet(WORKSHEET_NAME)
        
        data = wks.get_all_records()
        
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        
        # Ensure consistent columns even if empty
        expected_cols = ["type", "source", "details", "amount", "summary", "tags", "images", "created_at"]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = ""

        # Convert timestamp to datetime if possible for sorting
        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"], errors='coerce')

        return df
    except Exception as e:
        print(f"LOAD HISTORY ERROR: {e}")
        return pd.DataFrame()

def get_db_stats():
    """Returns basic stats about the history."""
    try:
        df = load_history()
        if df.empty: return {"total": 0}
        return {"total": len(df)}
    except:
        return {"total": 0}
