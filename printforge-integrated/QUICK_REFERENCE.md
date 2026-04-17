# 📋 PRINTFORGE - QUICK REFERENCE CARD

## 🎯 START HERE

### Choose Your Method:

**Option A: ONE-CLICK (Easiest)**
```
Windows: Double-click printforge-integrated\scripts\start_backend.bat
Linux/Mac: Run ./printforge-integrated/scripts/start_backend.sh
```

**Option B: COMMAND LINE**
```bash
cd printforge-integrated
scripts\start_backend.bat          # Windows
./scripts/start_backend.sh         # Linux/Mac
```

**Option C: DOCKER**
```bash
cd printforge-integrated
docker-compose up -d
```

---

## ✅ VERIFY IT'S RUNNING

Open in browser:
```
http://127.0.0.1:8000
```

You should see the **PrintForge login page**.

---

## 🔐 LOGIN CREDENTIALS

```
Email:    admin@printforge.com
Password: admin123
```

(Auto-created on first run)

---

## 📍 WHAT'S WHERE

| Component | File | Purpose |
|-----------|------|---------|
| **Backend** | `backend/main.py` | FastAPI (600+ lines) |
| **Frontend** | `frontend/index.html` | React UI (700+ lines) |
| **Config** | `config/.env` | Settings & Keys |
| **Start (Windows)** | `scripts/start_backend.bat` | Click to run |
| **Start (Linux/Mac)** | `scripts/start_backend.sh` | Run to start |
| **Docker** | `docker-compose.yml` | Container setup |

---

## 🌐 USEFUL URLS (When Running)

| What | URL |
|------|-----|
| **Frontend** | http://127.0.0.1:8000 |
| **API Docs** | http://localhost:8000/api/docs |
| **Health Check** | http://localhost:8000/api/health |

---

## 🛠️ COMMON COMMANDS

```bash
# Activate virtual environment
venv\Scripts\activate              # Windows
source venv/bin/activate           # Linux/Mac

# Install dependencies
pip install -r backend/requirements.txt

# Start backend (manual)
cd backend
python -m uvicorn main:app --reload --port 8000

# Stop backend
Ctrl+C

# Check if port is in use
netstat -ano | findstr :8000      # Windows
lsof -i :8000                      # Linux/Mac

# Kill process using port
taskkill /PID <PID> /F             # Windows
kill -9 <PID>                      # Linux/Mac
```

---

## 🐳 DOCKER COMMANDS

```bash
# Start containers
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop containers
docker-compose down

# Restart
docker-compose restart backend

# Full rebuild
docker-compose up -d --build
```

---

## 📁 PROJECT STRUCTURE

```
printforge-integrated/
├── backend/               ← FastAPI code here
│   ├── main.py
│   └── requirements.txt
├── frontend/              ← React code here
│   └── index.html
├── config/                ← Settings here
│   ├── .env
│   └── .env.example
├── scripts/               ← Startup scripts
│   ├── start_backend.bat
│   └── start_backend.sh
├── docs/                  ← Documentation
│   ├── README.md
│   ├── DEPLOYMENT.md
│   ├── QUICKSTART.md
│   └── OPERATION_GUIDE.md
├── Dockerfile             ← Docker setup
├── docker-compose.yml
└── README.md
```

---

## ⚡ QUICK TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Port 8000 in use | Kill process: `taskkill /PID <PID> /F` |
| Module not found | Activate venv & reinstall: `pip install -r backend/requirements.txt` |
| Database locked | Delete `printforge_brain.db` and restart |
| CORS error | Update `CORS_ORIGINS` in `config/.env` |
| Virtual environment not found | Run: `python -m venv venv` |
| Python not found | Install from python.org or check PATH |

---

## 📚 DOCUMENTATION

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `SETUP_SUMMARY.md` | Full setup guide (👈 Start here!) |
| `OPERATION_GUIDE.md` | How to run & deploy |
| `docs/QUICKSTART.md` | 30-second startup |
| `docs/DEPLOYMENT.md` | Production deployment guide |
| `docs/README.md` | Complete project docs |

---

## 🚀 DEPLOYMENT (When Ready)

### Simple (Render.com / Railway.app)
1. Push code to GitHub
2. Connect to platform
3. Auto-deploys

### Self-Hosted (VPS)
```bash
# SSH to server
# Clone repo
# Install Python
# Run: pip install -r backend/requirements.txt
# Use Gunicorn for production
```

See `docs/DEPLOYMENT.md` for detailed instructions.

---

## 🎯 FEATURES AVAILABLE

✅ User registration & login
✅ Product catalog & shopping cart
✅ Order management
✅ AI quote calculator
✅ Admin dashboard
✅ Product reviews & ratings
✅ Order tracking
✅ Quote history

---

## 📊 TECH STACK

- **Backend**: FastAPI / Uvicorn
- **Frontend**: React 18
- **Database**: SQLite
- **Auth**: JWT + bcrypt
- **Docs**: Swagger UI / ReDoc

---

## 🔐 DEFAULT CREDENTIALS

```
Admin Account (Created Automatically)
Email:    admin@printforge.com
Password: admin123
```

---

## 💾 DATABASE

**File**: `printforge_brain.db`
**Type**: SQLite
**Tables**: 6
- users
- products
- orders
- order_items
- reviews
- quotes

**Sample Data**: 3 products pre-loaded

---

## ⏱️ TIMING EXPECTATIONS

| Action | Time |
|--------|------|
| First startup | 2-3 min (installs packages) |
| Subsequent starts | 10-15 sec |
| Docker build | 1-2 min |
| Docker start | 5-10 sec |

---

## 🎓 FILE EDITING

### Edit Backend Code
```
File: backend/main.py
Changes: Auto-reload with --reload flag
Test: http://localhost:8000/api/docs
```

### Edit Frontend UI
```
File: frontend/index.html
Changes: Manual page refresh (Ctrl+R)
React code is inline in HTML
```

### Add Dependencies
```bash
pip install package_name
pip freeze > backend/requirements.txt
```

---

## 📞 SUPPORT

**Issue?** Check `docs/` folder:
- `docs/DEPLOYMENT.md` - Deployment issues
- `docs/QUICKSTART.md` - Quick reference
- `OPERATION_GUIDE.md` - Detailed operations
- `SETUP_SUMMARY.md` - Full setup

---

## ✨ THE 3-STEP PROCESS

```
1️⃣ Navigate to folder
   cd printforge-integrated

2️⃣ Start backend
   scripts\start_backend.bat

3️⃣ Open browser
   http://127.0.0.1:8000
```

**That's all you need!** 🎉

---

**Version**: 1.0.0 | **Status**: ✅ Production Ready
**Print this card & keep it handy!**
