# 🚀 Deployment & Running Guide - PrintForge + 3D Business Brain

## Project Structure Overview

```
printforge-integrated/
├── backend/                          # FastAPI Backend (Python)
│   ├── main.py                       # Main application file
│   └── requirements.txt               # Python dependencies
│
├── frontend/                         # React Frontend (Single HTML file)
│   └── index.html                    # Complete React app + UI
│
├── config/                           # Environment Configuration
│   ├── .env                          # Development environment variables
│   └── .env.example                  # Template for .env
│
├── scripts/                          # Startup Scripts
│   ├── start_backend.bat             # Windows backend startup
│   ├── start_backend.sh              # Linux/Mac backend startup
│   └── open_frontend.bat             # Frontend launcher
│
├── docs/                             # Documentation
│   └── README.md                     # Full project documentation
│
├── Docker Files (Root)               # Containerization
│   ├── Dockerfile                    # Docker image configuration
│   ├── docker-compose.yml            # Multi-container orchestration
│   └── .gitignore                    # Git exclusions
│
└── README.md                         # Project overview
```

---

## 🎯 Part 1: Running Locally (Development)

### Method 1️⃣: Windows Batch Script (Easiest)

**Step 1:** Open Command Prompt or PowerShell

**Step 2:** Navigate to project root
```batch
cd C:\Users\abhij\OneDrive\Desktop\brain\ 3d\printforge-integrated
```

**Step 3:** Run backend startup script
```batch
scripts\start_backend.bat
```

✅ **What this does:**
- Creates Python virtual environment (venv)
- Installs all dependencies
- Initializes SQLite database
- Starts FastAPI server at `http://localhost:8000`
- Shows API documentation at `http://localhost:8000/api/docs`

**Step 4:** Access the Application

In your browser, open one of:
- **Frontend**: http://127.0.0.1:8000
- **API Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

---

### Method 2️⃣: Linux/Mac Shell Script

**Step 1:** Open Terminal

**Step 2:** Navigate to project
```bash
cd ~/Desktop/"brain 3d"/printforge-integrated
```

**Step 3:** Make script executable & run
```bash
chmod +x scripts/start_backend.sh
./scripts/start_backend.sh
```

✅ **Same result as Windows method**

---

### Method 3️⃣: Manual Setup (Most Control)

**Windows:**
```batch
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Navigate to backend
cd backend

# Start server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Navigate to backend
cd backend

# Start server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

### Method 4️⃣: Docker (Containerized)

**Prerequisite:** Install Docker & Docker Compose

**Step 1:** Start containers
```bash
docker-compose up -d
```

**Step 2:** Check if running
```bash
docker-compose ps
```

**Step 3:** View logs
```bash
docker-compose logs -f backend
```

**Step 4:** Stop containers
```bash
docker-compose down
```

✅ **Backend runs at http://localhost:8000**

---

## 🔐 Default Login Credentials

Use these to login immediately:

```
📧 Email:    admin@printforge.com
🔑 Password: admin123
```

**This is an admin account with full dashboard access.**

---

## 🌐 Accessing the Application

### When Backend is Running:

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend** | http://127.0.0.1:8000 | Main user interface |
| **Swagger Docs** | http://localhost:8000/api/docs | Interactive API testing |
| **ReDoc Docs** | http://localhost:8000/api/redoc | Alternative API documentation |
| **Health Check** | http://localhost:8000/api/health | Backend status |

### What You Can Do:

✅ **Shop Tab** - Browse products, add to cart
✅ **AI Quote** - Calculate 3D printing costs
✅ **My Quotes** - View saved quotes
✅ **Cart** - Manage orders
✅ **Admin Dashboard** (if admin) - Manage inventory, view analytics

---

## 🛠️ Configuration

### Environment Variables (.env)

Located in: `config/.env`

```env
# Generate a secure key for production
SECRET_KEY=dev-secret-key-change-in-production

# Database path
DATABASE_PATH=printforge_brain.db

# API server URL
AI_SERVER_URL=http://127.0.0.1:8000

# Server configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS allowed origins
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000
```

**For Production:** Change these values before deploying!

---

## 📋 Troubleshooting

### ❌ Issue: "Port 8000 already in use"

**Windows:**
```batch
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -i :8000
kill -9 <PID>
```

---

### ❌ Issue: "Module not found" error

```bash
# Ensure venv is activated
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Reinstall dependencies
pip install -r backend/requirements.txt
```

---

### ❌ Issue: Database locked

**Development only - Safe to delete:**
```bash
# Remove database (development only!)
rm printforge_brain.db

# Restart - new database will be created automatically
```

---

### ❌ Issue: CORS errors in frontend

Update `CORS_ORIGINS` in `config/.env` to include your frontend URL:

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:8000,https://yourdomain.com
```

---

## 🚀 Part 2: Production Deployment

### Pre-Deployment Checklist

```
☐ Change SECRET_KEY to a secure random value
☐ Set DEBUG=False in .env
☐ Update CORS_ORIGINS to your production domain
☐ Use PostgreSQL instead of SQLite (optional but recommended)
☐ Set up HTTPS/SSL certificate
☐ Configure proper logging
☐ Set up database backups
☐ Test all API endpoints with production data
```

---

### Option A: Deploy on Render.com (Easiest)

**Step 1:** Create account at [render.com](https://render.com)

**Step 2:** Connect GitHub repository

**Step 3:** Create new Web Service
- Build Command: `pip install -r backend/requirements.txt`
- Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port 8000`

**Step 4:** Set Environment Variables
- Go to Environment → Add: `SECRET_KEY`, `DATABASE_PATH`, etc.

**Step 5:** Deploy
- Render automatically deploys when you push to git

✅ **Your app is live!** (URL provided by Render)

---

### Option B: Deploy on Railway.app

**Step 1:** Sign up at [railway.app](https://railway.app)

**Step 2:** Create new project from GitHub

**Step 3:** Add environment variables in dashboard

**Step 4:** Railway auto-detects Python and deploys

✅ **Live in minutes!**

---

### Option C: Deploy on Heroku

**Step 1:** Install Heroku CLI

**Step 2:** Login & create app
```bash
heroku login
heroku create your-app-name
```

**Step 3:** Add Procfile (root directory)
```
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Step 4:** Push to Heroku
```bash
git push heroku main
```

---

### Option D: Docker on AWS/DigitalOcean/Azure

**Step 1:** Build Docker image
```bash
docker build -t printforge:latest .
docker tag printforge:latest yourusername/printforge:latest
docker push yourusername/printforge:latest
```

**Step 2:** Deploy on cloud platform
- AWS ECS, DigitalOcean App Platform, or Azure Container Instances
- Use the pushed image

**Step 3:** Set environment variables in platform dashboard

---

### Option E: Self-Hosted VPS (DigitalOcean/Linode/Vultr)

**Step 1:** SSH into server
```bash
ssh root@your_server_ip
```

**Step 2:** Install dependencies
```bash
apt update && apt install python3-pip python3-venv nginx
```

**Step 3:** Clone repository
```bash
git clone <your-repo-url> printforge
cd printforge
```

**Step 4:** Setup & run
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Run with Gunicorn (production server)
pip install gunicorn
cd backend
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

**Step 5:** Setup Nginx reverse proxy
```bash
# Edit: /etc/nginx/sites-available/default
# Proxy traffic from port 80 to 8000
```

---

## 📊 Production Best Practices

### 1️⃣ Use PostgreSQL Instead of SQLite

For production, SQLite has limitations. Use PostgreSQL:

```bash
pip install psycopg2-binary
```

Update connection string:
```env
DATABASE_URL=postgresql://user:password@localhost/printforge
```

---

### 2️⃣ Use Gunicorn + Uvicorn Workers

For production:
```bash
pip install gunicorn

# Run with multiple workers
cd backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

---

### 3️⃣ Enable HTTPS

Get free SSL certificate from Let's Encrypt:

```bash
# Using Certbot
certbot certonly --standalone -d yourdomain.com
```

Configure in Nginx/Apache to use certificate.

---

### 4️⃣ Setup Monitoring & Logging

```bash
pip install python-json-logger
```

Monitor with:
- **Sentry.io** - Error tracking
- **New Relic** - Performance monitoring
- **DataDog** - Comprehensive monitoring

---

### 5️⃣ Database Backups

Automate daily backups:

```bash
# Backup SQLite (daily cron job)
0 2 * * * cp /path/to/printforge_brain.db /backups/backup_$(date +\%Y\%m\%d).db
```

---

## 🔄 Managing Application Lifecycle

### Restart Backend (Development)
```bash
# Press Ctrl+C in terminal running the server
# Then restart:
scripts\start_backend.bat  # Windows
./scripts/start_backend.sh # Linux/Mac
```

### Restart with Docker
```bash
docker-compose restart backend
```

### Update Code & Restart
```bash
git pull origin feature/printforge-integrated
docker-compose up -d --build
```

---

## 📈 Performance Tips

### Frontend Optimization
- ✅ Already using React 18 (optimized)
- ✅ Minified CSS included
- ✅ Single-page app (fast navigation)

### Backend Optimization
- ✅ SQLite with WAL mode (concurrent reads)
- ✅ Proper indexing on database tables
- ✅ Uvicorn with async/await

### Scale for Production
- Use multiple workers: `gunicorn -w 4`
- Add Redis caching layer
- Use load balancer (Nginx/HAProxy)
- Implement API rate limiting

---

## 📞 Getting Help

**API Not Responding?**
```bash
# Check backend health
curl http://localhost:8000/api/health
```

**Database Issues?**
```bash
# Check database file exists
ls -la printforge_brain.db

# Or on Windows:
dir printforge_brain.db
```

**Check Application Logs:**
```bash
# Docker logs
docker-compose logs -f backend

# Or look for errors in terminal where app was started
```

---

## Summary

| Phase | Method | Command |
|-------|--------|---------|
| **Development** | Quick Start | `scripts\start_backend.bat` |
| **Development** | Manual | `venv\Scripts\activate` then start server |
| **Development** | Docker | `docker-compose up -d` |
| **Production** | Render.com | Connect GitHub, auto-deploy |
| **Production** | Railway.app | Connect GitHub, auto-deploy |
| **Production** | Self-Hosted | Manual setup on VPS |

**Choose the method that fits your needs!**

---

**Version:** 1.0.0  
**Last Updated:** January 2024  
**Status:** Production Ready ✅
