# ⚡ Quick Start Guide - PrintForge

## 30-Second Startup

### Windows Users
```batch
cd printforge-integrated
scripts\start_backend.bat
```

### Linux/Mac Users
```bash
cd printforge-integrated
chmod +x scripts/start_backend.sh
./scripts/start_backend.sh
```

### Docker Users
```bash
cd printforge-integrated
docker-compose up -d
```

---

## That's It! 🎉

After running the above command:

1. **Backend starts automatically** at http://localhost:8000
2. **Database initializes** (SQLite)
3. **Admin account created** automatically

---

## Login Instantly

Open browser and go to: **http://127.0.0.1:8000**

Use demo account:
```
Email: admin@printforge.com
Password: admin123
```

---

## 📍 What You Get

✅ **Shopping Cart** - Add products, checkout  
✅ **AI Quote Calculator** - Calculate printing costs  
✅ **My Quotes** - Save & manage quotes  
✅ **Admin Dashboard** - View stats, manage orders  
✅ **Product Reviews** - Rate & review items  
✅ **User Accounts** - Register & login  

---

## 📍 API Documentation

When backend is running:
- **Interactive API Docs**: http://localhost:8000/api/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/api/redoc

Try API calls directly in the docs!

---

## 🔧 Common Issues

**Port 8000 in use?**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

**Module not found?**
```bash
# Make sure venv is activated
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r backend/requirements.txt
```

---

## 📚 Full Documentation

See `docs/DEPLOYMENT.md` for:
- Production deployment options (Render, Railway, Heroku, AWS)
- Advanced configuration
- Troubleshooting guide
- Performance optimization

---

## 🎯 Next Steps

1. ✅ Start backend (done above)
2. 🌐 Open http://127.0.0.1:8000 in browser
3. 🔐 Login with demo account
4. 🛒 Explore features
5. 📖 Read full docs for deployment

**Happy coding! 🚀**
