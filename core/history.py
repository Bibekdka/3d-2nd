import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os
import streamlit as st

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAME = "3d_brain_history"


def _get_sheet():
    creds_dict = None

    # Streamlit Secrets
    if "gcp_service_account" in st.secrets:
        creds_dict = dict(st.secrets["gcp_service_account"])

    # Render / Cloud ENV
    elif "gcp_service_account" in os.environ:
        creds_dict = json.loads(os.environ["gcp_service_account"])

    if not creds_dict:
        return None

    # Fix Render newline issue
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, SCOPE
    )
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet


def save_history(entry_type, title, data, notes):
    sheet = _get_sheet()
    if not sheet:
        return False

    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        entry_type,
        title,
        json.dumps(data),
        json.dumps(notes)
    ])
    return True


def load_history():
    sheet = _get_sheet()
    if not sheet:
        return []

    records = sheet.get_all_records()
    return records

def check_connection():
    return _get_sheet() is not None

def get_db_stats():
    history = load_history()
    if not history:
        return {"total": 0, "success_rate": 0}
    return {"total": len(history), "success_rate": 0} # Placeholder logic

def update_print_status(row_id, status):
    # Placeholder - Google Sheets row update logic would go here
    return True

def test_connection():
    try:
        sheet = _get_sheet()
        if not sheet:
            return False, "❌ Could not load credentials"

        # Simple read test
        headers = sheet.row_values(1)

        if not headers:
            return False, "⚠️ Sheet is accessible but headers are missing"

        return True, f"✅ Connected successfully. Headers: {headers}"

    except Exception as e:
        return False, f"❌ Connection failed: {e}"
