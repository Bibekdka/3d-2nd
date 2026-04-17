# 🚀 PrintForge + 3D Business Brain — Complete Integration Guide

## Overview

This integration combines:
- **PrintForge**: E-commerce marketplace with user auth, shopping, orders, admin dashboard
- **3D Business Brain**: AI analysis, quote calculator, STL processing
- **Result**: Single powerful platform for 3D printing business

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   FRONTEND (React Single Page)              │
│  ├─ Shop (Browse Products)                                 │
│  ├─ Product Detail + Reviews                               │
│  ├─ Shopping Cart & Checkout                               │
│  ├─ AI Quote Calculator (STL Upload)                       │
│  ├─ My Quotes (Manage Generated Quotes)                    │
│  ├─ My Orders                                               │
│  ├─ Admin Dashboard                                         │
│  └─ User Authentication (Register/Login)                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              BACKEND (FastAPI - main_integrated.py)         │
│  ├─ User Management (Register, Login, JWT)                 │
│  ├─ Product Catalog (CRUD + Ratings)                       │
│  ├─ Order Management (Create, Track)                       │
│  ├─ Quote System (Generate, Store, Accept)                 │
│  ├─ Admin Routes (Stats, Product Management)               │
│  ├─ STL Analysis (Trimesh for file processing)             │
│  └─ AI Integration (Calls local Ollama server)             │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                 DATABASES & EXTERNAL SERVICES               │
│  ├─ SQLite (printforge_brain.db) - All persistent data     │
│  ├─ AI Server (Ollama) - Optional AI analysis               │
│  └─ Google Sheets - Optional for reporting                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Files Overview

### New Files Created

| File | Purpose |
|------|---------|
| **main_integrated.py** | Combined FastAPI backend (commerce + AI) |
| **frontend_integrated.html** | Complete React frontend (no build needed) |
| **requirements_integrated.txt** | Updated Python dependencies |
| **INTEGRATION_GUIDE.md** | This file |

### Original Files (Still Used)

| File | Used For |
|------|----------|
| **local_ai_server.py** | Optional Ollama bridge (can run separately) |
| **config.py** | Optional configuration management |
| **.env.example** | Environment variables template |

---

## 🚀 Quick Start (Local Development)

### 1. Install Dependencies
```bash
pip install -r requirements_integrated.txt
```

### 2. Start Backend
```bash
python -m uvicorn main_integrated:app --reload
# API runs at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 3. Start Frontend
```bash
# Option A: Direct
open frontend_integrated.html

# Option B: Serve
python -m http.server 3000
# Then visit http://localhost:3000
```

### 4. (Optional) Start AI Server
```bash
python local_ai_server.py
# Runs at http://localhost:8000 (note: same port as API!)
```

### Default Admin Credentials
- Email: `admin@printforge.com`
- Password: `admin123`

---

## 🎯 Key Features

### For Customers

1. **Browse & Shop**
   - View all available products
   - Filter by category
   - Leave ratings and reviews
   - Add to cart and checkout

2. **AI Quote Calculator**
   - Upload STL files
   - Specify material, infill, profit margin
   - Get instant pricing
   - Save quotes for later

3. **Convert Quote to Product**
   - Accept generated quote
   - Convert to product listing
   - Customers can order

4. **Track Orders**
   - See order status
   - View order history

### For Admins

1. **Dashboard**
   - Revenue tracking
   - Order count
   - Quote management
   - Product inventory

2. **Product Management**
   - Add/edit/delete products
   - Manage stock
   - Set pricing
   - Upload images

3. **Order Management**
   - Update order status
   - Process shipments
   - View customer details

4. **Quote Management**
   - View all quotes
   - Accept/reject as products
   - Track quote-to-order conversion

---

## 🔌 API Endpoints Reference

### Authentication
```
POST   /auth/register          Create account
POST   /auth/login             Get JWT token
GET    /auth/me                Get current user
```

### Products
```
GET    /products               List all products
GET    /products/{id}          Get single product
GET    /products/{id}/reviews  Get product reviews
POST   /products/{id}/reviews  Add review (requires auth)
```

### Orders
```
POST   /orders                 Create order
GET    /orders/my              Get user's orders
```

### Quotes (NEW)
```
POST   /quotes                 Create quote
GET    /quotes/my              Get user's quotes
POST   /quotes/{id}/accept-as-product  Convert to product
```

### Admin
```
GET    /admin/products         List all products
POST   /admin/products         Add product
PUT    /admin/products/{id}    Edit product
DELETE /admin/products/{id}    Delete product
GET    /admin/orders           List all orders
PUT    /admin/orders/{id}/status  Update order status
GET    /admin/quotes           List all quotes
GET    /admin/stats            Get dashboard stats
```

### Health
```
GET    /health                 Check AI server + DB status
```

---

## 📊 Database Schema

### Users Table
```sql
id, name, email, password, is_admin, created_at
```

### Products Table
```sql
id, name, description, price, stock, category, material, 
print_time, weight_g, image_url, ai_analysis, is_quote, created_at
```

### Orders Table
```sql
id, user_id, total_amount, status, created_at
```

### Quotes Table (NEW)
```sql
id, user_id, file_name, weight_g, print_time, material_cost,
electricity_cost, labor_cost, subtotal, gst_amount, total,
status (pending/accepted/rejected/ordered), accepted_product_id, created_at
```

### Reviews Table
```sql
id, product_id, user_id, rating, comment, created_at
```

### Scraped Models Table (Optional)
```sql
id, user_id, url, title, description, ai_analysis, image_urls, created_at
```

---

## 🔧 Configuration

### Backend Configuration

Create `.env` file:
```bash
SECRET_KEY=your-secret-key-here
AI_SERVER_URL=http://127.0.0.1:8000  # Optional
DATABASE_URL=sqlite:///printforge_brain.db
```

### Frontend Configuration

Edit `frontend_integrated.html` line 8:
```javascript
const API = 'http://localhost:8000';  // Change to your deployed URL
```

---

## 📈 Workflow Examples

### Example 1: Customer Buys Pre-made Product
1. User browses shop
2. Selects product
3. Adds to cart
4. Checks out
5. Order created with "pending" status
6. Admin processes order

### Example 2: Customer Generates & Accepts Quote
1. User goes to "AI Quote Calculator"
2. Uploads STL file, configures settings
3. System calculates quote
4. User saves quote
5. After review, admin converts quote to product
6. Product now appears in shop
7. Can be purchased by others

### Example 3: Admin Issues Custom Quote
1. Admin logs in
2. Creates product manually in admin panel
3. Marks as "is_quote = 1"
4. Sets price and stock
5. Product appears in shop
6. Named "Custom Quote"

---

## 🌐 Deployment

### Option 1: Render.com (FREE - 15 min sleep)

**Backend:**
1. Push to GitHub
2. Render.com → New Web Service → Connect repo
3. **Build:** `pip install -r requirements_integrated.txt`
4. **Start:** `uvicorn main_integrated:app --host 0.0.0.0 --port $PORT`
5. Add env vars: `SECRET_KEY`, `AI_SERVER_URL`

**Frontend:**
1. Netlify, Vercel, or GitHub Pages
2. Update API URL in HTML
3. Deploy

### Option 2: Railway.app

Same as Render but $5/month free credit.

### Option 3: Docker

```bash
docker build -t printforge-brain .
docker run -p 8000:8000 \
  -e SECRET_KEY=your-key \
  -e AI_SERVER_URL=http://ai-server:8000 \
  printforge-brain
```

### Option 4: Self-Hosted

```bash
# Install PM2 for process management
npm install -g pm2

# Start backend
pm2 start "uvicorn main_integrated:app --host 0.0.0.0 --port 8000"

# Serve frontend with nginx
# Point nginx to frontend_integrated.html
```

---

## 🔒 Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Change admin password after first login
- [ ] Set CORS `allow_origins` to your domain only
- [ ] Use HTTPS in production
- [ ] Validate file uploads (STL files)
- [ ] Add rate limiting
- [ ] Enable logging
- [ ] Regular backups of SQLite database

---

## 🤖 AI Integration

### Optional Ollama/Local AI

1. **Install Ollama**
   ```bash
   # Download from ollama.ai
   ollama serve
   ```

2. **Pull Model**
   ```bash
   ollama pull phi3:mini
   ```

3. **Run Local AI Bridge**
   ```bash
   python local_ai_server.py
   ```

4. **Backend Will Use It**
   - AI analysis automatically called
   - Results stored in `products.ai_analysis`

### Fallback
If AI server is down:
- Quote calculator still works
- AI-based insights show "Analysis unavailable"
- System continues normally

---

## 📊 STL File Analysis

The system can now:
1. Accept `.stl` file uploads
2. Calculate volume, weight, print time
3. Estimate costs (material, electricity, labor)
4. Generate quote with profit margin
5. Include GST calculations
6. Convert to product

### Supported Materials
- PLA (1.24 g/cm³)
- PETG (1.27 g/cm³)
- ABS (1.04 g/cm³)
- TPU (1.21 g/cm³)
- Custom values supported

---

## 🐛 Troubleshooting

### "Connection Refused" Error
- Backend not running
- Check: `uvicorn main_integrated:app --reload`
- API should be at `http://localhost:8000`

### AI Functions Not Working
- AI server optional
- Work without it
- To enable: Run `python local_ai_server.py`
- Set `AI_SERVER_URL` in `.env`

### Database Locked
```bash
# Delete old lockfile
rm printforge_brain.db-wal
rm printforge_brain.db-shm
```

### File Upload Fails
- Check file size limits
- Only `.stl` files supported
- Check disk space

---

## 📝 Migration from Old System

If migrating from separate systems:

1. **Export old products** from Sheets
2. **Import to SQLite**
3. **Export user data** if available
4. **Migrate order history**
5. **Test quotes feature** with sample data
6. **Update frontend API URL**
7. **Deploy**

---

## 🚀 Next Steps

1. **Local Dev**
   - Run backend: `uvicorn main_integrated:app --reload`
   - Open `frontend_integrated.html`
   - Test all features

2. **AI Integration** (Optional)
   - Install Ollama
   - Run `python local_ai_server.py`
   - Test quote calculator with AI

3. **Customization**
   - Update colors/branding in HTML
   - Add your company info
   - Custom product categories

4. **Deployment**
   - Choose platform (Render, Railway, etc.)
   - Update configuration
   - Deploy frontend + backend
   - Test in production

5. **Admin Setup**
   - Add first batch of products
   - Set pricing
   - Customize descriptions
   - Add images

---

## 📞 Support

- **API Docs:** http://localhost:8000/docs (interactive Swagger)
- **Backend Issues:** Check logs in terminal
- **Frontend Issues:** Browser console (F12)
- **Database:** Check `printforge_brain.db`

---

## 🎉 You're All Set!

Your integrated 3D printing marketplace is ready to go. Start with local development, test all features, then deploy to production.

**Questions?** Check the `/docs` endpoint for full API documentation.
