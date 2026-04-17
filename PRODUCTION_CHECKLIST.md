# 📋 Production Readiness Checklist

Use this checklist to ensure your application is fully production-ready before deployment.

## ✅ Configuration & Secrets

- [ ] `.env` file created (copied from `.env.example`)
- [ ] `.env` configured with your environment settings
- [ ] `.streamlit/secrets.toml` created with Google Sheets credentials
- [ ] Google Cloud service account created and JSON downloaded
- [ ] Google Sheet named `printer_brain` created
- [ ] Service account email added with Sheets access
- [ ] No `.env` or `secrets.toml` files committed to git

## ✅ Local Development Testing

- [ ] Virtual environment created and activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Playwright installed: `playwright install chromium`
- [ ] Ollama installed and running: `ollama serve`
- [ ] Model pulled: `ollama pull phi3:mini`
- [ ] AI server running: `python local_ai_server.py`
- [ ] Streamlit app starts: `streamlit run app.py`
- [ ] All three tabs load without errors:
  - [ ] Intelli-DB tab
  - [ ] Quote Calculator tab
  - [ ] System Health tab
- [ ] Database connection shows "ONLINE"
- [ ] AI server shows "online" in Health tab
- [ ] Web scraping works with test URL
- [ ] Quote calculator works with test STL file
- [ ] No errors in console or app.log

## ✅ Code Quality

- [ ] No hardcoded secrets in code
- [ ] All API calls use retry logic
- [ ] Logging statements throughout
- [ ] Error handling for all network calls
- [ ] Input validation on user inputs
- [ ] Configuration managed via `config.py`
- [ ] No `print()` statements (use logger instead)
- [ ] All imports organized

## ✅ Docker & Containerization

- [ ] Dockerfile created and tested locally
- [ ] docker-compose.yml configured
- [ ] Docker image builds successfully
- [ ] Container runs without errors
- [ ] Health checks pass
- [ ] Volume mounts work correctly

## ✅ Documentation

- [ ] README.md is complete and accurate
- [ ] PRODUCTION_GUIDE.md reviewed
- [ ] PRODUCTION_READY.md reviewed
- [ ] DEPLOYMENT.md is up-to-date
- [ ] Inline code comments clear
- [ ] Setup instructions tested and working

## ✅ Logging & Monitoring

- [ ] Logging configured in `config.py`
- [ ] Log level set to INFO for production
- [ ] Logs written to `app.log`
- [ ] No sensitive data in logs
- [ ] Log rotation configured (if applicable)
- [ ] Error logs are detailed and actionable

## ✅ Security

- [ ] `.gitignore` includes all sensitive files
- [ ] DEBUG mode is false in production config
- [ ] API endpoints validate input
- [ ] Timeouts set on all network calls
- [ ] No API keys exposed in code
- [ ] Error messages don't leak system info
- [ ] CORS configured appropriately
- [ ] HTTPS enabled (if required by platform)

## ✅ Performance

- [ ] Caching enabled for repeated queries
- [ ] Database queries optimized
- [ ] Image processing doesn't cause memory issues
- [ ] Scraper has reasonable timeouts
- [ ] AI analysis doesn't timeout on normal inputs
- [ ] App loads in <5 seconds

## ✅ Testing

- [ ] Database: Can add/read/display entries
- [ ] Scraper: Successfully extracts from multiple sites
- [ ] AI: Analyzes text and generates tags
- [ ] Calculator: Accurate cost calculations
- [ ] Health: All status checks responsive
- [ ] Error handling: Graceful failure without crashes

## ✅ Deployment Specific

### For Render.com
- [ ] GitHub repo connected
- [ ] Environment variables set in Render dashboard
- [ ] Secrets configured in Render
- [ ] Build command includes playwright install
- [ ] Start command is correct
- [ ] Resource allocation sufficient
- [ ] Health check endpoint configured

### For Docker/Self-Hosted
- [ ] Image built successfully
- [ ] Container starts without errors
- [ ] Port mappings correct
- [ ] Volume mounts working
- [ ] Network connectivity tested
- [ ] Logs accessible

### For Cloud Run / Heroku
- [ ] Deployment credentials configured
- [ ] Environment variables set
- [ ] Secrets available to container
- [ ] Memory allocation sufficient
- [ ] Startup time acceptable

## ✅ Post-Deployment

- [ ] App accessible at deployment URL
- [ ] All tabs load correctly
- [ ] Database connection works
- [ ] AI server responding
- [ ] Web scraping functional
- [ ] Logs are being generated
- [ ] No errors in platform logs
- [ ] Health dashboard shows all green

## ✅ Monitoring Plan

- [ ] Set up log monitoring/alerts
- [ ] Configure health check monitoring
- [ ] Set up error notification
- [ ] Document incident response procedure
- [ ] Backup strategy in place
- [ ] Scaling strategy defined

## ⚠️ Common Issues to Verify

### Database Issues
- [ ] Correct sheet name configured
- [ ] Service account has access
- [ ] credentials JSON is valid
- [ ] Network connectivity to Google APIs
- [ ] Worksheet headers are correct

### AI Server Issues
- [ ] Ollama is installed
- [ ] Model is downloaded
- [ ] No port conflicts (8000)
- [ ] Server is responding to health checks
- [ ] Timeout values are reasonable

### Scraper Issues
- [ ] Playwright is installed
- [ ] Chromium browser available
- [ ] Network access working
- [ ] URL parsing handles redirects
- [ ] Memory sufficient for large pages

## 📝 Notes

Use this space to document any custom setup:

```
- Environment: _______________
- Platform: _______________
- Custom modifications: _______________
- Known issues: _______________
```

## ✨ Final Sign-Off

- [ ] All checklist items completed
- [ ] Ready for production deployment
- [ ] Monitoring configured
- [ ] Team trained on operation
- [ ] Disaster recovery plan in place

**Date: _______________**
**Approved by: _______________**
**Version: 1.0.0**

---

For detailed information, refer to:
- [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) - Comprehensive deployment guide
- [README.md](README.md) - Project overview
- [PRODUCTION_READY.md](PRODUCTION_READY.md) - What changed for production
