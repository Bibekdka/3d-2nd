# Deployment Guide

Your 3D Brain application is **Production Ready** and uses **Google Sheets** for permanent storage!

## 📦 Key Configuration

| File | Purpose |
| :--- | :--- |
| `requirements.txt` | Python dependencies (updated for GSheets). |
| `packages.txt` | System dependencies for Playwright (Critical for Cloud). |
| `app.py` | Main entry point. |
| `database.py` | Database logic (Now uses **Google Sheets**). |
| `.streamlit/secrets.toml` | **CRITICAL**: Contains Google Service Account credentials. |

## 🚀 deployment Option: Render.com

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
    *   `STREAMLIT_SECRETS_PATH`: `/etc/secrets/secrets.toml` (See step 6 below).
    *   `STREAMLIT_SAFE_MODE`: `false`
    *   **Note**: You DO NOT need to add `GROK_API_KEY` here if you include it in the secrets file below. If not, add it here.

6.  **Secret Files (CRITICAL STEP)**:
    Render does not read `.streamlit/secrets.toml` from your repo (it's ignored). You must add it manually.
    *   Go to your Render Dashboard -> **"Secret Files"** tab (or "Environment" -> "Secret Files").
    *   Click **"Add Secret File"**.
    *   **Filename**: `secrets.toml`
    *   **Content**: Copy the ENTIRE content of your local `.streamlit/secrets.toml`.
        *   (This includes the `[gsheets]` section AND the `OPENAI_API_KEY` / `GROK_API_KEY`).
    *   Click **Save**.

    *Why `/etc/secrets/secrets.toml`?*
    Render mounts secret files to `/etc/secrets/<filename>`. By setting `STREAMLIT_SECRETS_PATH` to this location in Step 5, Streamlit will find your keys.

## ☁️ Option: Streamlit Community Cloud

1.  **Deploy**: Connect your GitHub repo.
2.  **Advanced Settings**:
    *   Go to **Secrets** section.
    *   Paste the content of your local `.streamlit/secrets.toml`.
    *   Save.
3.  **Deploy**.
