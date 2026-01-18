# Deployment Guide

Your 3D Brain application is **Production Ready**!

## 📦 Key Configuration

| File | Purpose |
| :--- | :--- |
| `requirements.txt` | Python dependencies (updated for Grok). |
| `packages.txt` | System dependencies for Playwright (Critical for Cloud). |
| `app.py` | Main entry point. |
| `scaper.py` | Web scraper (Respects `STREAMLIT_SAFE_MODE`). |
| `brain.db` | SQLite database (Persists locally, resets on cloud redeploy unless using persistent disk). |

## 🚀 Option A: Streamlit Cloud (Easiest)

1.  **Push Code**: Ensure your code is on GitHub (you already pushed to `3d-2nd`).
2.  **New App**: Go to [share.streamlit.io](https://share.streamlit.io).
3.  **Settings**:
    *   **Repository**: `your-username/3d-2nd`
    *   **Main File**: `app.py`
4.  **Advanced Settings (Secrets)**:
    *   Add your API keys here:
        ```toml
        GROK_API_KEY = "xai-..."
        AI_PROVIDER = "grok"
        ```
5.  **Deploy**: Click **Deploy**.

## ☁️ Option B: Render.com (Robust)

1.  **New Web Service**: Connect your GitHub repo.
2.  **Runtime**: Python 3.
3.  **Build Command**:
    ```bash
    pip install -r requirements.txt && playwright install chromium
    ```
4.  **Start Command**:
    ```bash
    streamlit run app.py
    ```
5.  **Environment Variables**:
    *   `GROK_API_KEY`: `xai-...`
    *   `AI_PROVIDER`: `grok`
    *   `STREAMLIT_SAFE_MODE`: `false` (Set to `true` if scraper fails).

## ⚠️ Important Note on Database
Since we are using **SQLite (`brain.db`)**:
*   On **Streamlit Cloud**: The database will **reset** if the app goes to sleep or reboots.
*   On **Render**: The database will **reset** on every deployment unless you attach a **Persistent Disk**.

**Production Recommendation**: For permanent data storage, switch `database.py` to use **Google Sheets** (which we had before) or a cloud database like **Supabase** or **Render PostgreSQL** in the future.
