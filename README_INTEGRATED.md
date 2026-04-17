# 🚀 PrintForge + 3D Business Brain — Integrated Platform

**Complete 3D Printing Marketplace with AI-Powered Quote Generation**

---

## ✨ What You Get

### 🛒 E-Commerce Features
- ✅ Product catalog with inventory management
- ✅ User registration & authentication (JWT)
- ✅ Shopping cart & checkout
- ✅ Order tracking and status management
- ✅ Product reviews and ratings
- ✅ Admin dashboard with analytics

### 🤖 AI + Analysis Features  
- ✅ STL file upload and analysis
- ✅ Automatic cost calculation
- ✅ Material/electricity/labor cost breakdown
- ✅ Profit margin management with GST
- ✅ Quote generation and storage
- ✅ Convert quotes to products
- ✅ Optional Ollama AI integration for insights

### 💼 Business Management
- ✅ Quote management system
- ✅ Product lifecycle (quote → product → order)
- ✅ Revenue tracking
- ✅ Inventory management
- ✅ Admin panel with full control

---

## 🎯 Quick Start

### 1 Minute Setup

```bash
# Windows
start_integrated.bat

# Linux/macOS
bash start_integrated.sh
```

Then open `frontend_integrated.html` in your browser.

**Default Admin Login:**
- Email: `admin@printforge.com`
- Password: `admin123`

---

## 📁 New Integrated Files

| File | Purpose |
|------|---------|
| **main_integrated.py** | Complete FastAPI backend (commerce + AI) |
| **frontend_integrated.html** | Full React frontend in one file |
| **requirements_integrated.txt** | Python dependencies |
| **start_integrated.bat** | Windows startup script |
| **start_integrated.sh** | Linux/macOS startup script |
| **INTEGRATION_GUIDE.md** | Detailed technical documentation |

---

## 🏗️ Architecture

```
Frontend (Single HTML file - React)
    ↓
FastAPI Backend (main_integrated.py)
    ├─ User Management
    ├─ Product Catalog
    ├─ Orders & Quotes
    ├─ STL Analysis (Trimesh)
    └─ AI Integration (Optional)
    ↓
SQLite Database (printforge_brain.db)
```

### Technology Stack
- **Frontend:** React 18 (single HTML file, no build)
- **Backend:** FastAPI + Uvicorn
- **Database:** SQLite (zero configuration)
- **Authentication:** JWT tokens
- **File Processing:** Trimesh for STL analysis
- **Optional:** Ollama for local AI

---

## 🎮 How It Works

### For Customers

1. **Browse & Shop** - See all available products
2. **AI Quote Calculator** - Upload STL, get instant pricing
3. **Save Quotes** - Store quotes for later review
4. **Order** - Buy products or accept quotes
5. **Track** - Follow order status

### For Admin

1. **Manage Products** - Add/edit/delete inventory
2. **Process Orders** - Change status (pending → shipped → delivered)
3. **Manage Quotes** - Accept quotes as products
4. **View Analytics** - Revenue, orders, products stats
5. **Change Passwords** - First thing to do!

---

## 🚀 Deployment

### Heroku (Simplest)
```bash
heroku create your-app
git push heroku main
```

### Render.com
1. Connect GitHub repo
2. Build: `pip install -r requirements_integrated.txt`
3. Start: `uvicorn main_integrated:app --host 0.0.0.0 --port $PORT`

### Railway.app
Same as Render, simpler pricing.

### Docker
```bash
docker build -t printforge .
docker run -p 8000:8000 printforge
```

See **INTEGRATION_GUIDE.md** for full deployment details.

---

## 📊 Key Features Deep Dive

### Quote Calculator
1. Upload STL file
2. Set material, infill, walls
3. Configure costs (filament, electricity, labor)
4. Set profit margin & GST
5. Get instant quote
6. Save for approval

### Quote to Product Conversion
1. Admin reviews quote
2. Converts to product listing
3. Sets stock level
4. Now available for customers to order
5. Tracked as "custom quote" product

### Orders System
Statuses: `pending` → `processing` → `shipped` → `delivered`

### Reviews & Ratings
Customers can:
- Rate products (1-5 stars)
- Leave comments
- View others' reviews

---

## 🔧 Configuration

### Environment Variables (.env)
```
SECRET_KEY=your-secret-key-here
AI_SERVER_URL=http://127.0.0.1:8000
DATABASE_PATH=printforge_brain.db
```

### Frontend API URL
Edit `frontend_integrated.html` line 8:
```javascript
const API = 'http://localhost:8000';  // Change for production
```

---

## 📈 File Upload Workflow

```
Customer uploads STL
        ↓
Trimesh analyzes file
        ↓
Calculate volume, weight, dimensions
        ↓
Estimate print time
        ↓
Calculate costs (material + electricity + labor)
        ↓
Apply profit margin
        ↓
Add GST
        ↓
Generate final quote
        ↓
Customer reviews & accepts
        ↓
Quote saved to database
        ↓
Admin can convert to product
        ↓
Product available to shop
```

---

## 🔒 Security

- JWT token-based authentication
- Password hashing with bcrypt
- Admin-only endpoints protected
- CORS configurable per domain
- SQLite with WAL mode for data integrity
- No sensitive data in frontend code

---

## 🤖 Optional AI Integration

### Setup Local Ollama
```bash
# Install from ollama.ai
ollama serve

# Pull model (in another terminal)
ollama pull phi3:mini

# Start AI bridge
python local_ai_server.py
```

Works without AI, but enabled for:
- Product analysis insights
- Quote recommendations
- Customer chat (future)

---

## 📖 API Documentation

After starting backend, visit: **http://localhost:8000/docs**

Interactive Swagger documentation with:
- Try-it-out functionality
- Request/response schemas
- All endpoints documented
- Authentication examples

---

## 🐛 Troubleshooting

### Can't install dependencies
```bash
# Use specific Python version
python3.11 -m pip install -r requirements_integrated.txt
```

### Port 8000 already in use
```bash
# Windows: Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac: Run on different port
python -m uvicorn main_integrated:app --port 8001
```

### SQLite database locked
```bash
rm printforge_brain.db-wal
rm printforge_brain.db-shm
```

### Frontend can't reach backend
- Check API URL in line 8 of HTML
- Ensure backend is running
- Check for CORS issues in console

---

## 📊 Database Schema

**9 Tables:**
- `users` - Customers and admins
- `products` - Catalog items
- `orders` - Customer orders
- `order_items` - Order line items
- `reviews` - Product ratings/comments
- `quotes` - Generated pricing quotes
- `scraped_models` - Optional web scrapes
- Plus indexes for performance

---

## 🎨 Customization

### Change Colors
Edit CSS variables in `frontend_integrated.html`:
```javascript
--accent: #e8f55a;      // Yellow
--accent2: #ff6b35;     // Orange
--bg: #0a0a0b;          // Dark background
```

### Add New Product Categories
Backend automatically handles categories from products table.

### Extend with More Fields
Add columns to database, update schema, modify frontend forms.

---

## 📞 Support & Documentation

1. **API Docs:** http://localhost:8000/docs
2. **Technical Guide:** INTEGRATION_GUIDE.md
3. **Code Comments:** Throughout main_integrated.py
4. **Frontend:** Comments in frontend_integrated.html

---

## 🚢 Production Checklist

- [ ] Change `SECRET_KEY` to random string
- [ ] Change admin password
- [ ] Set `CORS allow_origins` to your domain
- [ ] Enable HTTPS (handled by deployment platform)
- [ ] Set up database backups
- [ ] Configure error logging
- [ ] Test all payment flows
- [ ] Verify email notifications (for future)
- [ ] Load test with sample data
- [ ] Set up monitoring

---

## 🔄 Workflow Examples

### Example 1: Buy Pre-Made Product
```
Browse Shop → Find Product → Add to Cart → Checkout → Order Created
```

### Example 2: Generate & Order Custom Quote
```
AI Calculator → Upload STL → Configure Settings → Generate Quote → Save
→ (Later) → Accept Quote → Converts to Product → Order Placed
```

### Example 3: Admin Workflow
```
Login (admin@printforge.com) → Dashboard → View Stats → Manage Orders
→ Customer Places Order → Update Status → Mark as Shipped → View Revenue
```

---

## 💡 Pro Tips

1. **Test with Sample STL** - Create a simple cube for testing
2. **Use Different Browsers** - Test cross-browser compatibility
3. **Monitor API Logs** - Check uvicorn output for issues
4. **Backup Database** - Copy printforge_brain.db regularly
5. **Test Admin Features** - Add products before going live

---

## 🎯 Next Steps

1. **Local Testing** ✓
   - Start backend & frontend
   - Test user registration
   - Try quote calculator
   - Test admin dashboard

2. **Customize** 
   - Update colors/branding
   - Add your products
   - Configure pricing
   - Test payment flow

3. **Deploy**
   - Choose platform (Render, Railway, etc.)
   - Deploy backend API
   - Deploy frontend
   - Configure domain
   - Enable HTTPS

4. **Scale**
   - Migrate to PostgreSQL if needed
   - Add caching layer
   - Set up CDN for images
   - Implement analytics

---

## 📄 License

[Specify your license]

---

## 🙋 Questions?

Check:
1. **API Docs:** http://localhost:8000/docs
2. **Integration Guide:** INTEGRATION_GUIDE.md
3. **Error Messages:** Check browser console (F12)
4. **Backend Logs:** Check terminal output

---

## 🎉 You're Ready to Launch!

Your complete 3D printing marketplace is ready. Start locally, test thoroughly, then deploy to production.

**Happy printing! 🖨️**
