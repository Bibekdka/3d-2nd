# ============================================================
#  PrintForge + 3D Business Brain — Integrated Backend
#  FastAPI + SQLite
#  Location: printforge-integrated/backend/
# ============================================================

import os
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import sqlite3, json, io
import requests
import trimesh
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / "config" / ".env")

# ── CONFIG ────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_IN_PRODUCTION_supersecret123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
DB_PATH = os.getenv("DATABASE_PATH", "printforge_brain.db")
AI_SERVER_URL = os.getenv("AI_SERVER_URL", "http://127.0.0.1:8000")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

app = FastAPI(
    title="PrintForge + 3D Business Brain API",
    version="1.0.0",
    description="Complete 3D printing marketplace with AI analysis",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── SECURITY ──────────────────────────────────────────────────
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def hash_password(p): 
    return pwd_ctx.hash(p)

def verify_password(plain, hashed): 
    return pwd_ctx.verify(plain, hashed)

def create_token(data: dict):
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)

# ── DATABASE SETUP ────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database with all tables"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        email       TEXT    UNIQUE NOT NULL,
        password    TEXT    NOT NULL,
        is_admin    INTEGER DEFAULT 0,
        created_at  TEXT    DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS products (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        description TEXT,
        price       REAL    NOT NULL,
        stock       INTEGER DEFAULT 0,
        category    TEXT,
        material    TEXT,
        print_time  TEXT,
        weight_g    REAL,
        image_url   TEXT,
        ai_analysis TEXT,
        is_quote    INTEGER DEFAULT 0,
        created_at  TEXT    DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS orders (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id      INTEGER NOT NULL REFERENCES users(id),
        total_amount REAL    NOT NULL,
        status       TEXT    DEFAULT 'pending',
        created_at   TEXT    DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS order_items (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id    INTEGER NOT NULL REFERENCES orders(id),
        product_id  INTEGER NOT NULL REFERENCES products(id),
        product_name TEXT   NOT NULL,
        quantity    INTEGER NOT NULL,
        price       REAL    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS reviews (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id  INTEGER NOT NULL REFERENCES products(id),
        user_id     INTEGER NOT NULL REFERENCES users(id),
        rating      INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
        comment     TEXT,
        created_at  TEXT    DEFAULT (datetime('now')),
        UNIQUE(product_id, user_id)
    );

    CREATE TABLE IF NOT EXISTS quotes (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL REFERENCES users(id),
        file_name   TEXT    NOT NULL,
        weight_g    REAL,
        print_time  REAL,
        material_cost REAL,
        electricity_cost REAL,
        labor_cost  REAL,
        subtotal    REAL    NOT NULL,
        gst_amount  REAL,
        total       REAL    NOT NULL,
        status      TEXT    DEFAULT 'pending',
        accepted_product_id INTEGER REFERENCES products(id),
        created_at  TEXT    DEFAULT (datetime('now'))
    );
    """)
    conn.commit()

    # Seed admin user if empty
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count == 0:
        conn.execute("INSERT INTO users (name, email, password, is_admin) VALUES (?,?,?,1)",
                     ("Admin", "admin@printforge.com", hash_password("admin123")))
        conn.commit()

    # Seed sample products
    count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count == 0:
        sample_products = [
            ("Miniature Dragon", "Highly detailed fantasy dragon figurine", 349, 15, "Figurines", "PLA", "6hr", 85, "https://images.unsplash.com/photo-1612036781124-5f5b9bd6e7a8?w=400", None, 0),
            ("Cable Organizer Set", "Desk cable management clips", 149, 50, "Organizers", "PETG", "2hr", 30, "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400", None, 0),
            ("Phone Stand", "Adjustable phone holder for all phones", 199, 25, "Accessories", "PLA", "3hr", 55, "https://images.unsplash.com/photo-1586105251261-72a756497a11?w=400", None, 0),
        ]
        conn.executemany(
            "INSERT INTO products (name, description, price, stock, category, material, print_time, weight_g, image_url, ai_analysis, is_quote) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            sample_products
        )
        conn.commit()
    conn.close()

# ── HELPER FUNCTIONS ──────────────────────────────────────────
def row_to_dict(row):
    return dict(row) if row else None

def rows_to_list(rows):
    return [dict(r) for r in rows]

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_admin(user=Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# ── PYDANTIC SCHEMAS ──────────────────────────────────────────
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category: Optional[str] = None
    material: Optional[str] = None
    print_time: Optional[str] = None
    weight_g: Optional[float] = None
    image_url: Optional[str] = None

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItem]

class ReviewCreate(BaseModel):
    rating: int
    comment: Optional[str] = None

class StatusUpdate(BaseModel):
    status: str

class QuoteCreate(BaseModel):
    file_name: str
    weight_g: float
    print_time: float
    material_cost: float
    electricity_cost: float
    labor_cost: float
    subtotal: float
    gst_amount: float
    total: float

# ── AUTH ROUTES ───────────────────────────────────────────────
@app.post("/api/auth/register")
def register(data: UserRegister, db=Depends(get_db)):
    if db.execute("SELECT id FROM users WHERE email = ?", (data.email,)).fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")
    db.execute("INSERT INTO users (name, email, password) VALUES (?,?,?)",
               (data.name, data.email, hash_password(data.password)))
    db.commit()
    return {"message": "Account created successfully"}

@app.post("/api/auth/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = db.execute("SELECT * FROM users WHERE email = ?", (form.username,)).fetchone()
    if not user or not verify_password(form.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": str(user["id"])})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/auth/me")
def me(user=Depends(get_current_user)):
    return {"id": user["id"], "name": user["name"], "email": user["email"], "is_admin": bool(user["is_admin"])}

# ── PRODUCT ROUTES ────────────────────────────────────────────
def enrich_products(products, db):
    """Attach ratings to products"""
    result = []
    for p in products:
        d = dict(p)
        stats = db.execute(
            "SELECT AVG(rating) as avg_r, COUNT(*) as cnt FROM reviews WHERE product_id = ?", (d["id"],)
        ).fetchone()
        d["avg_rating"] = round(stats["avg_r"] or 0, 1) if stats else 0
        d["review_count"] = stats["cnt"] if stats else 0
        result.append(d)
    return result

@app.get("/api/products")
def list_products(db=Depends(get_db)):
    products = db.execute("SELECT * FROM products WHERE stock > 0 ORDER BY created_at DESC").fetchall()
    return enrich_products(products, db)

@app.get("/api/products/{product_id}")
def get_product(product_id: int, db=Depends(get_db)):
    p = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return enrich_products([p], db)[0]

@app.get("/api/products/{product_id}/reviews")
def get_reviews(product_id: int, db=Depends(get_db)):
    rows = db.execute("""
        SELECT r.*, u.name as user_name FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.product_id = ?
        ORDER BY r.created_at DESC
    """, (product_id,)).fetchall()
    return rows_to_list(rows)

@app.post("/api/products/{product_id}/reviews")
def add_review(product_id: int, data: ReviewCreate, user=Depends(get_current_user), db=Depends(get_db)):
    if not 1 <= data.rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be 1–5")
    try:
        db.execute(
            "INSERT INTO reviews (product_id, user_id, rating, comment) VALUES (?,?,?,?)",
            (product_id, user["id"], data.rating, data.comment)
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="You've already reviewed this product")
    return {"message": "Review added"}

# ── ORDER ROUTES ──────────────────────────────────────────────
@app.post("/api/orders")
def create_order(data: OrderCreate, user=Depends(get_current_user), db=Depends(get_db)):
    if not data.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    order_items = []

    for item in data.items:
        p = db.execute("SELECT * FROM products WHERE id = ?", (item.product_id,)).fetchone()
        if not p:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if p["stock"] < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {p['name']}")
        total += p["price"] * item.quantity
        order_items.append((item.product_id, p["name"], item.quantity, p["price"]))

    cur = db.execute("INSERT INTO orders (user_id, total_amount) VALUES (?,?)", (user["id"], total))
    order_id = cur.lastrowid

    for prod_id, prod_name, qty, price in order_items:
        db.execute("INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES (?,?,?,?,?)",
                   (order_id, prod_id, prod_name, qty, price))
        db.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, prod_id))

    db.commit()
    return {"message": "Order placed", "order_id": order_id}

@app.get("/api/orders/my")
def my_orders(user=Depends(get_current_user), db=Depends(get_db)):
    orders = db.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC", (user["id"],)).fetchall()
    result = []
    for o in orders:
        d = dict(o)
        items = db.execute("SELECT * FROM order_items WHERE order_id = ?", (o["id"],)).fetchall()
        d["items"] = rows_to_list(items)
        result.append(d)
    return result

# ── QUOTE ROUTES ──────────────────────────────────────────────
@app.post("/api/quotes")
def create_quote(data: QuoteCreate, user=Depends(get_current_user), db=Depends(get_db)):
    cur = db.execute("""
        INSERT INTO quotes 
        (user_id, file_name, weight_g, print_time, material_cost, electricity_cost, labor_cost, subtotal, gst_amount, total, status)
        VALUES (?,?,?,?,?,?,?,?,?,?, 'pending')
    """, (user["id"], data.file_name, data.weight_g, data.print_time, data.material_cost, 
          data.electricity_cost, data.labor_cost, data.subtotal, data.gst_amount, data.total))
    db.commit()
    return {"message": "Quote saved", "quote_id": cur.lastrowid}

@app.get("/api/quotes/my")
def my_quotes(user=Depends(get_current_user), db=Depends(get_db)):
    quotes = db.execute("SELECT * FROM quotes WHERE user_id = ? ORDER BY created_at DESC", (user["id"],)).fetchall()
    return rows_to_list(quotes)

# ── ADMIN ROUTES ──────────────────────────────────────────────
@app.get("/api/admin/products")
def admin_list_products(admin=Depends(require_admin), db=Depends(get_db)):
    products = db.execute("SELECT * FROM products ORDER BY created_at DESC").fetchall()
    return enrich_products(products, db)

@app.post("/api/admin/products", status_code=201)
def admin_add_product(data: ProductCreate, admin=Depends(require_admin), db=Depends(get_db)):
    cur = db.execute(
        "INSERT INTO products (name, description, price, stock, category, material, print_time, weight_g, image_url) VALUES (?,?,?,?,?,?,?,?,?)",
        (data.name, data.description, data.price, data.stock, data.category, data.material, data.print_time, data.weight_g, data.image_url)
    )
    db.commit()
    return {"message": "Product added", "id": cur.lastrowid}

@app.put("/api/admin/products/{product_id}")
def admin_update_product(product_id: int, data: ProductCreate, admin=Depends(require_admin), db=Depends(get_db)):
    p = db.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    db.execute("""
        UPDATE products SET name=?, description=?, price=?, stock=?, category=?,
        material=?, print_time=?, weight_g=?, image_url=? WHERE id=?
    """, (data.name, data.description, data.price, data.stock, data.category,
          data.material, data.print_time, data.weight_g, data.image_url, product_id))
    db.commit()
    return {"message": "Product updated"}

@app.delete("/api/admin/products/{product_id}")
def admin_delete_product(product_id: int, admin=Depends(require_admin), db=Depends(get_db)):
    db.execute("DELETE FROM products WHERE id = ?", (product_id,))
    db.commit()
    return {"message": "Product deleted"}

@app.get("/api/admin/orders")
def admin_list_orders(admin=Depends(require_admin), db=Depends(get_db)):
    orders = db.execute("""
        SELECT o.*, u.email as user_email FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.created_at DESC
    """).fetchall()
    result = []
    for o in orders:
        d = dict(o)
        items = db.execute("SELECT * FROM order_items WHERE order_id = ?", (o["id"],)).fetchall()
        d["items"] = rows_to_list(items)
        result.append(d)
    return result

@app.put("/api/admin/orders/{order_id}/status")
def admin_update_order_status(order_id: int, data: StatusUpdate, admin=Depends(require_admin), db=Depends(get_db)):
    valid = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    if data.status not in valid:
        raise HTTPException(status_code=400, detail=f"Status must be one of {valid}")
    db.execute("UPDATE orders SET status = ? WHERE id = ?", (data.status, order_id))
    db.commit()
    return {"message": "Order status updated"}

@app.get("/api/admin/stats")
def admin_stats(admin=Depends(require_admin), db=Depends(get_db)):
    total_revenue = db.execute("SELECT COALESCE(SUM(total_amount),0) FROM orders WHERE status != 'cancelled'").fetchone()[0]
    total_orders = db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    total_products = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    total_quotes = db.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]

    rev_by_status = {}
    for row in db.execute("SELECT status, COALESCE(SUM(total_amount),0) as rev FROM orders GROUP BY status").fetchall():
        rev_by_status[row["status"]] = row["rev"]

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_products": total_products,
        "total_quotes": total_quotes,
        "revenue_by_status": rev_by_status,
    }

# ── HEALTH CHECK ────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {
        "status": "online",
        "database": "sqlite",
        "version": "1.0.0"
    }

# ── ROOT ────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "PrintForge + 3D Business Brain API",
        "docs": "/api/docs",
        "version": "1.0.0"
    }

# ── STARTUP ───────────────────────────────────────────────────
@app.on_event("startup")
def startup():
    init_db()
    print("✅ PrintForge + 3D Business Brain API Started")
    print("📊 Database: " + DB_PATH)
    print("🔑 Default Admin: admin@printforge.com / admin123")
    print("📖 Docs: http://localhost:8000/api/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
