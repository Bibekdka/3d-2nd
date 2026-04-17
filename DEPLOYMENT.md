# Deployment Guide

Your 3D Brain application is **Production Ready** and uses **Google Sheets** for permanent storage!

## 📦 Key Configuration

| File | Purpose |
| :--- | :--- |
| `requirements.txt` | Python dependencies (updated for production). |
| `.streamlit/config.toml` | Streamlit production configuration. |
| `config.py` | Centralized configuration management. |
| `.env.example` | Environment variable template. |
| `app.py` | Main entry point. |
| `database.py` | Database logic (Google Sheets). |
| `.streamlit/secrets.toml` | **CRITICAL**: Contains Google Service Account credentials. |
| `PRODUCTION_GUIDE.md` | **[READ THIS]** Complete production deployment guide. |

## 🚀 Quick Start

### 1. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Copy env template
cp .env.example .env

# Install Playwright (for scraper)
playwright install chromium

# Run app
streamlit run app.py

# In another terminal, run AI server
python local_ai_server.py
```

### 2. Production Deployment

**See [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) for:**
- Complete setup instructions
- Platform-specific deployment (Render, Docker, Cloud Run)
- Secrets management
- Monitoring & logging
- Troubleshooting

### 3. Environment Variables

See `.env.example` for configuration template.

## deployment Option: Render.com

1.  **New Web Service**: Connect your GitHub repo.
2.  **Runtime**: Python 3.11
3.  **Build Command**:
    ```bash
    pip install -r requirements.txt && playwright install chromium
    ```
4.  **Start Command**:
    ```bash
    streamlit run app.py
    ```
5.  **Environment Variables**:
    *   `APP_ENV`: `production`
    *   `DEBUG`: `false`
    *   `LOG_LEVEL`: `INFO`

6.  **Secrets** (Set via Render dashboard):
    *   Add the `gsheets` configuration from `.streamlit/secrets.toml`

## ✅ Production Checklist

- [ ] Environment variables configured
- [ ] Google Sheets API credentials set up
- [ ] AI server deployed or configured
- [ ] Database connection tested
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Health check passing

## 📊 Health Status

Check the **System Health** tab in the app for:
- Database connection status
- AI server availability
- Model information
- Detailed diagnostics

## 🔍 Logging

Logs are written to `app.log` (local) or platform logs (production).

Check for issues:
```bash
tail -f app.log | grep ERROR
```

## 🆘 Support

For detailed troubleshooting, see [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)

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
