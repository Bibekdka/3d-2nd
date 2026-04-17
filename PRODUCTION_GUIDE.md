# 🚀 Production Deployment Guide

## Overview
Your 3D Business Brain application is now production-ready. This guide covers deployment, configuration, monitoring, and best practices.

---

## 📋 Pre-Deployment Checklist

- [ ] All environment variables configured (`.env` file)
- [ ] Google Sheets API credentials set up and verified
- [ ] Ollama/AI server running or configured
- [ ] SSL certificate configured (if using custom domain)
- [ ] Backup strategy in place
- [ ] Monitoring/logging configured
- [ ] Error handling tested

---

## 🔧 Configuration

### 1. Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

**Critical variables:**
```bash
APP_ENV=production
DEBUG=false
LOCAL_AI_URL=http://your-ai-server:8000
LOG_LEVEL=INFO
```

### 2. Google Sheets API Setup

1. Create service account in [Google Cloud Console](https://console.cloud.google.com/)
2. Download JSON credentials
3. Create `.streamlit/secrets.toml`:

```toml
[gsheets]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@example.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

4. Create Google Sheet named `printer_brain`
5. Share with service account email
6. In Streamlit Cloud, add to Environment secrets

### 3. Ollama/AI Server

**Local deployment (single machine):**
```bash
ollama serve
# In another terminal:
python local_ai_server.py
```

**Docker deployment:**
```dockerfile
FROM ollama/ollama:latest
RUN ollama pull phi3:mini

# AI API server in separate container
FROM python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY local_ai_server.py .
ENV LOCAL_AI_URL=http://ollama:11434
CMD ["python", "local_ai_server.py"]
```

---

## 🌐 Deployment Platforms

### Option 1: Render.com (Recommended for Streamlit)

1. **Create new Web Service**
   - Select your GitHub repo
   - Runtime: Python 3.11
   
2. **Build Command**
   ```bash
   pip install -r requirements.txt && playwright install chromium
   ```

3. **Start Command**
   ```bash
   streamlit run app.py
   ```

4. **Environment Variables**
   ```
   APP_ENV=production
   DEBUG=false
   LOG_LEVEL=INFO
   ```

5. **Secrets**
   - Add `gsheets` secret (JSON from Google Cloud)
   - Add any other sensitive configuration

6. **Scaling**
   - Set to "Standard" or higher for production
   - Enable auto-scaling if needed

### Option 2: Docker + Cloud Run (Google Cloud)

```bash
# Build image
docker build -t brain-3d .

# Deploy to Cloud Run
gcloud run deploy brain-3d \
  --image brain-3d \
  --platform managed \
  --region us-central1 \
  --set-env-vars APP_ENV=production \
  --memory 2Gi
```

### Option 3: Heroku

```bash
# Create app
heroku create brain-3d

# Configure
heroku config:set APP_ENV=production
heroku config:set DISABLE_COLLECTSTATIC=1

# Deploy
git push heroku main
```

---

## 📊 Monitoring & Logging

### Log Locations
- **Local:** `app.log` in project directory
- **Production:** Check platform's logs
  - Render: Dashboard → Logs
  - Cloud Run: Cloud Logging
  - Heroku: `heroku logs --tail`

### Health Checks

Monitor these endpoints:
- `/health` - Main app health (Streamlit doesn't expose this directly)
- AI Server: `GET http://ai-server:8000/health`
- Database: Check Google Sheets access via Health tab in app

### Recommended Monitoring

```python
# View logs in production
tail -f app.log | grep ERROR
```

---

## 🔒 Security Best Practices

### 1. Secrets Management
- ✅ Use platform secret management (Render, Cloud Run)
- ✅ Never commit `.env` or `secrets.toml`
- ❌ Don't hardcode credentials
- ❌ Don't share API keys in code

### 2. API Security
- Add rate limiting to AI server (if exposed)
- Use HTTPS only (platform should enforce)
- Validate all inputs
- Enable CORS only for trusted origins

### 3. Database Security
- Use service account with minimal permissions
- Restrict Google Sheet access to specific email
- Enable 2FA on Google account
- Regularly audit sheet access

### 4. Error Handling
- Production mode disables detailed error messages
- Check logs for detailed error information
- User sees generic "Error" message in UI
- Set `DEBUG=false` in production

---

## 🚨 Troubleshooting

### AI Server Not Responding
```bash
# Check if running
ps aux | grep ollama

# Test connectivity
curl http://localhost:8000/health

# Check logs
tail -f app.log | grep "ai_server"
```

### Database Connection Failed
1. Verify Google Sheets API credentials
2. Ensure service account has access
3. Check internet connectivity
4. Review `app.log` for detailed error

### Memory Issues
- Increase platform memory allocation
- Limit scraper image downloads
- Enable caching (enabled by default)

### Slow Performance
- Check database query frequency
- Consider caching layer
- Monitor AI server response times
- Profile with platform monitoring tools

---

## 📈 Performance Optimization

### Caching
Enabled by default. Configure in `config.py`:
```python
ENABLE_CACHE = True
CACHE_TTL_SECONDS = 3600
```

### Database Optimization
- Limit query results
- Archive old records
- Use indexes in Google Sheets
- Consider pagination

### AI Server Optimization
- Use faster model (`mistral:7b-instruct-q4_K_M`)
- Increase timeout for complex queries
- Implement queue system for high traffic

---

## 🔄 Deployment Workflow

### 1. Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Run locally
streamlit run app.py

# In another terminal
python local_ai_server.py
```

### 2. Staging
Deploy to staging environment before production.

### 3. Production
```bash
git add .
git commit -m "Production deployment"
git push origin main
# Platform auto-deploys
```

### 4. Monitoring
Check logs and health status after deployment.

---

## 📚 Additional Resources

- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Render Deployment Guide](https://render.com/docs/deploy-streamlit)
- [Google Cloud SQL Setup](https://cloud.google.com/sql/docs/postgres/quickstart)
- [Ollama Models](https://ollama.ai/library)

---

## 🆘 Support

For issues:
1. Check `app.log` for detailed error messages
2. Use Health tab in app for diagnostics
3. Review platform-specific logs
4. Enable DEBUG mode temporarily (development only)

---

## Version History

- **v1.0.0** (2024-04-17): Production-ready release
  - Added centralized configuration
  - Implemented logging throughout
  - Added retry logic for API calls
  - Enhanced error handling
  - Added production deployment guide
