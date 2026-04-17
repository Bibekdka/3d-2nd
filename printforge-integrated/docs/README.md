# PrintForge + 3D Business Brain

## Project Overview

**PrintForge** is a comprehensive 3D printing marketplace platform integrated with AI-powered quote generation and advanced business analytics.

### Key Features

#### 🛍️ E-Commerce Marketplace
- Product catalog with search and filtering
- Shopping cart and checkout system
- Order management and tracking
- Customer reviews and ratings
- Inventory management

#### 🤖 AI Quote Calculator
- Intelligent cost estimation for 3D printing projects
- Automatic material, labor, and electricity cost calculation
- GST (Tax) computation
- Quote persistence and history tracking
- Quote-to-product conversion workflow

#### 👥 User Management
- User registration and authentication
- JWT-based secure sessions
- User profile management
- Admin dashboard for business operations

#### 📊 Admin Dashboard
- Real-time statistics and analytics
- Revenue tracking by order status
- Order management interface
- Product management tools
- Customer quote requests

---

## Project Structure

```
printforge-integrated/
├── backend/                      # FastAPI Backend
│   ├── main.py                  # Main application file (FastAPI)
│   └── requirements.txt          # Python dependencies
│
├── frontend/                     # React Frontend
│   └── index.html               # Single-file React application
│
├── config/                       # Configuration & Secrets
│   ├── .env                     # Development environment (gitignored)
│   └── .env.example             # Template for .env
│
├── docs/                         # Documentation
│   ├── README.md                # This file
│   ├── SETUP.md                 # Setup & Installation
│   ├── API_DOCS.md              # API Documentation
│   └── DEPLOYMENT.md            # Production Deployment
│
├── scripts/                      # Startup Scripts
│   ├── start_backend.bat        # Windows backend startup
│   ├── start_backend.sh         # Linux/Mac backend startup
│   └── open_frontend.bat        # Frontend launcher
│
├── Dockerfile                    # Docker containerization
├── docker-compose.yml            # Multi-container setup
├── .gitignore                    # Git exclusions
└── README.md                     # Main project README
```

---

## Quick Start (Development)

### Prerequisites
- **Python 3.8+** (for backend)
- **Node.js** (optional, for frontend build tools)
- **Git** for version control

### Installation & Running

**Option 1: Windows Users**
```batch
cd scripts
start_backend.bat
```

This will:
1. Create a Python virtual environment
2. Install all dependencies
3. Initialize the database
4. Start the FastAPI server at `http://localhost:8000`

**Option 2: Linux/Mac Users**
```bash
cd scripts
chmod +x start_backend.sh
./start_backend.sh
```

**Option 3: Manual Setup**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Run backend
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Option 4: Docker**
```bash
docker-compose up -d
```

---

## Accessing the Application

### Backend API
- **URL**: http://localhost:8000
- **API Docs (Swagger UI)**: http://localhost:8000/api/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/api/redoc

### Frontend (Browser)
- **URL**: http://127.0.0.1:8000/api or open `frontend/index.html` directly in browser

### Default Admin Credentials
```
Email: admin@printforge.com
Password: admin123
```

---

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **Database**: SQLite (with WAL mode for production)
- **Authentication**: JWT + bcrypt
- **3D Processing**: Trimesh
- **API Docs**: Swagger UI / ReDoc

### Frontend
- **Framework**: React 18 (via CDN)
- **Styling**: Custom CSS with gradients
- **State Management**: React Hooks
- **HTTP**: Fetch API

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Version Control**: Git

---

## API Endpoints Overview

### Authentication
```
POST   /api/auth/register    - Register new user
POST   /api/auth/login       - User login (returns JWT token)
GET    /api/auth/me          - Get current user info
```

### Products
```
GET    /api/products         - List all active products
GET    /api/products/{id}    - Get product details
GET    /api/products/{id}/reviews - Get product reviews
POST   /api/products/{id}/reviews - Add product review
```

### Orders
```
POST   /api/orders           - Create new order
GET    /api/orders/my        - Get user's orders
```

### Quotes
```
POST   /api/quotes           - Create new quote
GET    /api/quotes/my        - Get user's quotes
```

### Admin
```
GET    /api/admin/stats      - Dashboard statistics
GET    /api/admin/products   - List all products (with stock)
POST   /api/admin/products   - Add new product
PUT    /api/admin/products/{id} - Update product
DELETE /api/admin/products/{id} - Delete product
GET    /api/admin/orders     - List all orders
PUT    /api/admin/orders/{id}/status - Update order status
```

---

## Database Schema

### Tables
1. **users** - User accounts and authentication
2. **products** - Product catalog
3. **orders** - Customer orders
4. **order_items** - Items in each order
5. **reviews** - Product reviews and ratings
6. **quotes** - AI-generated quotes

All tables support:
- Foreign key constraints
- Automatic timestamps
- Transaction support

---

## Configuration

### Environment Variables (.env)

```env
# API Configuration
SECRET_KEY=your-secret-key-here
DATABASE_PATH=printforge_brain.db
AI_SERVER_URL=http://127.0.0.1:8000

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI Integration (Optional)
OLLAMA_MODEL=mistral
OLLAMA_HOST=http://127.0.0.1:11434
```

---

## Development Workflow

### Adding New Features
1. Create new route in `backend/main.py`
2. Define Pydantic schema for request/response
3. Implement database operations
4. Update `frontend/index.html` with new UI component
5. Test via Swagger UI at `/api/docs`

### Running Tests
```bash
# pytest can be added to requirements.txt
pip install pytest
pytest backend/
```

### Code Style
- Use type hints throughout
- Follow PEP 8 conventions
- Use meaningful variable names
- Add docstrings for complex functions

---

## Production Deployment

### Pre-Deployment Checklist
- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False`
- [ ] Update `CORS_ORIGINS` for production domain
- [ ] Backup database
- [ ] Review all environment variables
- [ ] Test all API endpoints
- [ ] Set up SSL/TLS certificate

### Deployment Platforms Supported
- **Render.com** - Easy Python/Docker deployment
- **Railway.app** - Git-integrated deployment
- **Heroku** - Traditional PaaS option
- **AWS** - EC2, ECS, Lambda options
- **DigitalOcean** - VPS or App Platform
- **Vercel** (Frontend only)

### Docker Deployment
```bash
# Build image
docker build -t printforge:latest .

# Run container
docker run -p 8000:8000 -e SECRET_KEY=prod-key printforge:latest

# Or use docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

---

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Database Locked
- Delete `printforge_brain.db` and restart (development only)
- Check for stuck processes using the database

### Module Not Found
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### CORS Errors
- Update `CORS_ORIGINS` in `.env` to include your domain
- Ensure frontend is running on allowed origin

---

## Contributing

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make changes and test
3. Commit with clear messages: `git commit -m "Add feature description"`
4. Push to branch: `git push origin feature/your-feature`
5. Create Pull Request

---

## Security Notes

### Current Limitations (Development)
- Passwords stored with bcrypt (production-safe)
- JWT expires after 7 days
- SQLite suitable for small-medium applications
- No rate limiting implemented (add with python-slowapi)

### Production Recommendations
- Use PostgreSQL instead of SQLite
- Implement rate limiting
- Add HTTPS enforced
- Use environment-based secrets management
- Implement audit logging
- Add request validation for all inputs
- Set up automated backups

---

## License

This project is provided as-is for development and commercial use.

---

## Support

For issues or questions:
1. Check existing documentation in `/docs`
2. Review API documentation at `/api/docs`
3. Check database logs for error messages
4. Verify all environment variables are set correctly

---

**Updated**: January 2024
**Version**: 1.0.0
**Status**: Production Ready
