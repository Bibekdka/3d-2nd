# 📦 PrintForge + 3D Business Brain

Complete 3D printing e-commerce marketplace with AI-powered quote generation system.

## 🎯 Quick Start

**Windows:**
```batch
cd scripts
start_backend.bat
```

**Linux/Mac:**
```bash
cd scripts
chmod +x start_backend.sh
./start_backend.sh
```

**Docker:**
```bash
docker-compose up -d
```

Then visit: **http://localhost:8000**

## 📖 Demo Credentials

```
Email: admin@printforge.com
Password: admin123
```

## ✨ Features

- 🛍️ **E-Commerce Marketplace** - Product catalog, shopping cart, orders
- 🤖 **AI Quote Calculator** - Smart cost estimation for 3D printing
- 👥 **User Management** - Registration, authentication, profiles
- 📊 **Admin Dashboard** - Analytics, order management, inventory
- ⭐ **Reviews & Ratings** - Customer feedback system
- 🔐 **Secure Auth** - JWT tokens, bcrypt passwords
- 🐳 **Dockerized** - Easy deployment with Docker Compose
- 📱 **Responsive UI** - React 18 single-page application

## 🏗️ Project Structure

```
printforge-integrated/
├── backend/          # FastAPI backend (Python)
├── frontend/         # React frontend (HTML/CSS/JS)
├── config/          # Environment & secrets
├── docs/            # Documentation
├── scripts/         # Startup scripts
└── docker-compose.yml
```

## 🚀 Deployment

- **Development**: `start_backend.bat` or `start_backend.sh`
- **Docker**: `docker-compose up`
- **Production**: See [DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 📚 Documentation

- [README.md](docs/README.md) - Full project documentation
- [SETUP.md](docs/SETUP.md) - Detailed setup instructions
- [API_DOCS.md](docs/API_DOCS.md) - API reference
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Production deployment

## 🔧 Tech Stack

**Backend:**
- FastAPI 0.104.1
- SQLite
- JWT Authentication
- Uvicorn Server

**Frontend:**
- React 18
- Responsive CSS
- Fetch API

**DevOps:**
- Docker
- Docker Compose
- Git

## 📝 License

This project is provided as-is for development and commercial use.

---

**Version:** 1.0.0 | **Status:** ✅ Production Ready
