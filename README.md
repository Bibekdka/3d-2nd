# 🧠 3D Business Brain

A production-ready Streamlit application for intelligent 3D printing business management. Combines web scraping, AI analysis, intelligent quote generation, and Google Sheets integration.

## ✨ Features

- **🕵️ Intelligent Web Scraper** - Extract and analyze 3D models from Printables, Thingiverse, MakerWorld
- **🤖 AI-Powered Analysis** - Local Ollama integration for model risk assessment and optimization
- **💼 Smart Quote Calculator** - STL analysis, cost calculation, profit margin management
- **📊 Knowledge Base** - Google Sheets integration for persistent data storage
- **🩺 System Health Dashboard** - Real-time monitoring of AI and database connectivity
- **📈 Business Economics** - Material costs, electricity, labor, GST calculations

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Ollama (for AI features)
- Google Cloud service account (for database)
- Git

### Local Development (Windows)
```bash
# Double-click to run
start_dev.bat

# In another terminal
start_ai.bat
```

### Local Development (Linux/macOS)
```bash
bash start_dev.sh

# In another terminal
python local_ai_server.py
```

### Docker
```bash
docker-compose up --build
```

## 📋 Setup Instructions

### 1. Environment Configuration

```bash
cp .env.example .env
# Edit .env with your configuration
```

Key variables:
- `APP_ENV` - development, staging, or production
- `LOCAL_AI_URL` - AI server URL (default: http://127.0.0.1:8000)
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

### 2. Google Sheets Setup

1. Create a [Google Cloud project](https://console.cloud.google.com/)
2. Enable Google Sheets API
3. Create a service account and download JSON credentials
4. Create `.streamlit/secrets.toml`:

```toml
[gsheets]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "..."
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

5. Create a Google Sheet named `printer_brain`
6. Share it with the service account email

### 3. AI Server Setup

**Using Ollama (Recommended):**
```bash
# Install Ollama from https://ollama.ai/
ollama serve

# In another terminal, pull the model
ollama pull phi3:mini

# Start the AI bridge
python local_ai_server.py
```

## 📁 Project Structure

```
brain-3d/
├── app.py                    # Main Streamlit application
├── database.py               # Google Sheets integration
├── ai.py                     # AI server client & retry logic
├── scraper.py                # Web scraping functionality
├── app_utils.py              # STL analysis & cost calculations
├── local_ai_server.py        # Local Ollama bridge API
├── config.py                 # Centralized configuration
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── .streamlit/
│   ├── config.toml           # Production settings
│   └── secrets.example.toml  # Secrets template
├── Dockerfile                # Docker image
├── docker-compose.yml        # Local development stack
├── DEPLOYMENT.md             # Quick deployment guide
├── PRODUCTION_GUIDE.md       # Production deployment details
└── README.md                 # This file
```

## 🎯 Usage

### 1. Add Intelligence (Web Scraping)
- Paste a URL from Printables, Thingiverse, or MakerWorld
- Click "Analyze" to extract and analyze
- AI processes the model for risks and optimization
- Save to knowledge base

### 2. Calculate Quotes
- Upload one or more STL files
- Configure printer, material, infill, profit margin
- App calculates material cost, electricity, labor
- Generate customer invoice with GST

### 3. Monitor System Health
- View database connection status
- Check AI server connectivity and model
- View error logs for troubleshooting

## 📊 Configuration Options

### Printer Profiles
- Ender 3 / V2 (Speed: 50mm/s, 350W)
- Bambu P1/X1 (Speed: 120mm/s, 1000W)
- Prusa MK3/4 (Speed: 70mm/s, 200W)

### Materials
- PLA (Density: 1.24 g/cm³)
- PETG (Density: 1.27 g/cm³)
- ABS (Density: 1.04 g/cm³)
- TPU (Density: 1.21 g/cm³)

## 🔍 Logging

Logs are written to `app.log` with detailed information about:
- Database operations
- AI server health checks and analysis
- Web scraping activities
- Errors and warnings

Check logs:
```bash
tail -f app.log
grep ERROR app.log
```

## 🛠️ Development

### Running Tests Locally
```bash
# With all services
docker-compose up

# Visit http://localhost:8501
```

### Code Structure

**app.py** - Main UI with three tabs:
- Intelli-DB: Web scraping and knowledge base
- Quote Calculator: STL analysis and pricing
- System Health: Diagnostics and monitoring

**database.py** - Google Sheets operations:
- Authentication via service account
- CRUD operations for knowledge base
- Data persistence

**ai.py** - AI server interaction:
- Health checks with retry logic
- Model analysis with timeout handling
- Automatic retries on failure

**scraper.py** - Web scraping:
- Playwright-based browser automation
- Image extraction and filtering
- Text content cleaning

## 🚀 Deployment

### Render.com (Recommended)

1. Connect GitHub repository
2. Set Runtime to Python 3.11
3. Build Command: `pip install -r requirements.txt && playwright install chromium`
4. Start Command: `streamlit run app.py`
5. Add environment variables and secrets

See [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) for detailed instructions.

### Docker

```bash
docker build -t brain-3d .
docker run -p 8501:8501 \
  -e APP_ENV=production \
  -e LOCAL_AI_URL=http://host.docker.internal:8000 \
  brain-3d
```

## 🔒 Security

- ✅ Secrets stored in `.streamlit/secrets.toml` (not in code)
- ✅ Environment variables for all configuration
- ✅ Retry logic with exponential backoff
- ✅ Error hiding in production mode
- ✅ Input validation and sanitization
- ✅ HTTPS enforced in production

**Never commit:**
- `.env` files
- `.streamlit/secrets.toml`
- API keys or credentials
- Database passwords

## 📝 Logging Levels

- `DEBUG` - Detailed information for debugging
- `INFO` - General informational messages
- `WARNING` - Warning messages for noteworthy events
- `ERROR` - Error messages for serious problems

Set in `.env`:
```
LOG_LEVEL=INFO
```

## 🐛 Troubleshooting

### AI Server Connection Failed
```bash
# Check if Ollama is running
ps aux | grep ollama

# Test connectivity
curl http://localhost:8000/health

# View AI server logs
tail -f app.log | grep "ai_server"
```

### Database Connection Failed
1. Verify Google Sheets API credentials
2. Check service account has access
3. Ensure sheet name is correct
4. Review `app.log` for detailed error

### Scraper Timeout
- Increase `SCRAPER_TIMEOUT` in `.env`
- Check internet connectivity
- Verify URL is valid

## 📚 Additional Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Ollama Models](https://ollama.ai/library)
- [Render Deployment](https://render.com/docs)

## 📄 License

[Specify your license here]

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
1. Check [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)
2. Review application logs
3. Use System Health tab to diagnose
4. Enable DEBUG mode for detailed logging

## 🎉 Version

**v1.0.0** - Production Release
- Centralized configuration system
- Comprehensive logging
- Retry logic for resilience
- Docker support
- Production deployment guides
