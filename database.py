import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials
from config import get_logger, SHEET_NAME, WORKSHEET_NAME

logger = get_logger("database")

# --- CONFIGURATION ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

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
        error_msg = "Missing '[gsheets]' section in secrets.toml"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None

    try:
        creds_dict = dict(st.secrets["gsheets"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        client = gspread.authorize(creds)
        logger.info("gspread client authenticated successfully")
        return client
    except Exception as e:
        error_msg = f"Authentication failed: {str(e)}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None

# --- CORE FUNCTIONS ---
def check_connection():
    """Checks if we can access the Google Sheet."""
    if "gsheets" not in st.secrets:
        return {"status": False, "error": "Configuration Missing"}
        
    try:
        client = get_gspread_client()
        if not client: 
            return {"status": False, "error": "Auth Failed"}
        
        # Try to open the sheet
        sh = client.open(SHEET_NAME)
        logger.info(f"Database connection verified for sheet '{SHEET_NAME}'")
        return {"status": True, "error": None}
    except gspread.SpreadsheetNotFound as e:
        error_msg = f"Sheet '{SHEET_NAME}' not found"
        logger.error(error_msg)
        return {"status": False, "error": error_msg}
    except Exception as e:
        error_msg = f"DB CONNECTION ERROR: {str(e)}"
        logger.error(error_msg)
        return {"status": False, "error": str(e)}

def init_db():
    """
    Ensures the target Sheet and Worksheet exist with correct headers.
    """
    try:
        client = get_gspread_client()
        if not client: 
            logger.error("Failed to initialize DB: No client")
            return

        try:
            sh = client.open(SHEET_NAME)
            logger.info(f"Sheet '{SHEET_NAME}' opened")
        except gspread.SpreadsheetNotFound:
            error_msg = f"Google Sheet '{SHEET_NAME}' not found. Please create it and share with the service account email."
            logger.error(error_msg)
            st.error(f"❌ {error_msg}")
            return

        try:
            wks = sh.worksheet(WORKSHEET_NAME)
            logger.info(f"Worksheet '{WORKSHEET_NAME}' found")
        except gspread.WorksheetNotFound:
            logger.info(f"Creating new worksheet '{WORKSHEET_NAME}'")
            wks = sh.add_worksheet(title=WORKSHEET_NAME, rows=100, cols=10)
            wks.append_row(["type", "source", "details", "amount", "summary", "tags", "images", "created_at"])
            logger.info("Worksheet initialized with headers")
            
    except Exception as e:
        error_msg = f"DB INIT ERROR: {str(e)}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")

def add_entry(type_, source, details, amount, summary, tags, images=None):
    """
    Appends a new row to the history worksheet with error handling.
    """
    try:
        client = get_gspread_client()
        if not client:
            logger.error(f"Cannot add entry {type_}: No client")
            return False

        sh = client.open(SHEET_NAME)
        wks = sh.worksheet(WORKSHEET_NAME)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Handle optional images
        if images is None: 
            images = []
        images_str = str(images) if isinstance(images, list) else str(images)
        
        # Validate required fields
        if not type_ or not source or not summary:
            logger.warning(f"Incomplete entry: type={type_}, source={source}, summary={summary}")
            st.error("Missing required fields (type, source, or summary)")
            return False
        
        # Append row
        wks.append_row([type_, source, details, amount, summary, tags, images_str, timestamp])
        logger.info(f"Entry added: {type_} | {source} | {timestamp}")
        return True
    except gspread.exceptions.APIError as e:
        error_msg = f"Google Sheets API Error: {str(e)}"
        logger.error(error_msg)
        st.error(f"Failed to save: {error_msg}")
        return False
    except Exception as e:
        error_msg = f"ADD ENTRY ERROR: {str(e)}"
        logger.error(error_msg)
        st.error(f"Failed to save: {error_msg}")
        return False

def load_history():
    """
    Fetches all records from the sheet and returns a pandas DataFrame.
    """
    try:
        client = get_gspread_client()
        if not client: 
            logger.warning("Cannot load history: No client")
            return pd.DataFrame()

        sh = client.open(SHEET_NAME)
        wks = sh.worksheet(WORKSHEET_NAME)
        
        data = wks.get_all_records()
        logger.info(f"Loaded {len(data)} records from database")
        
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
        error_msg = f"LOAD HISTORY ERROR: {str(e)}"
        logger.error(error_msg)
        return pd.DataFrame()

def get_db_stats():
    """Returns basic stats about the history."""
    try:
        df = load_history()
        if df.empty: 
            return {"total": 0}
        count = len(df)
        logger.info(f"Database stats: {count} total entries")
        return {"total": count}
    except Exception as e:
        logger.error(f"Error getting DB stats: {str(e)}")
        return {"total": 0}
