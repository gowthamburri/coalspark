# ⚡ Quick Reference - CoalSpark Restaurant

## 🚀 Start Application (Daily Use)

### Terminal 1 - Backend
```bash
cd coalspark/backend
venv\Scripts\activate
uvicorn main:app --reload
```
✅ http://localhost:8000

### Terminal 2 - Frontend
```bash
cd coalspark/frontend
npm run dev
```
✅ http://localhost:5173

---

## 🔐 Default Login

**Admin:**
- Email: `admin@coalspark.in`
- Password: `admin1234`

---

## 📚 Important URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | Main application |
| Backend API | http://localhost:8000 | API server |
| Swagger Docs | http://localhost:8000/docs | API testing UI |
| ReDoc | http://localhost:8000/redoc | API documentation |

---

## 🛠️ Common Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"

# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Frontend
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

---

## 📁 Key Files

### Backend
- `main.py` - FastAPI entry point
- `.env` - Environment variables
- `alembic.ini` - Migration config
- `requirements.txt` - Python deps

### Frontend
- `src/App.jsx` - React root component
- `package.json` - Node dependencies
- `vite.config.js` - Vite configuration
- `tailwind.config.js` - Tailwind CSS config

---

## 🐛 Quick Fixes

### Port in use?
```bash
# Kill process on Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Use different port
uvicorn main:app --port 8001
npm run dev -- --port 5174
```

### Dependencies issue?
```bash
# Backend
pip install -r requirements.txt --upgrade

# Frontend
rmdir /s /q node_modules
npm install
```

### Database reset?
```bash
# Delete SQLite database
del app.db

# Recreate tables
alembic upgrade head
```

---

## 🎯 Feature Checklist

### Customer Features
- ✅ Browse menu by categories
- ✅ Search dishes
- ✅ Add to cart
- ✅ Place orders
- ✅ View order history

### Admin Features
- ✅ Dashboard stats
- ✅ Manage menu (CRUD)
- ✅ Upload images
- ✅ Update order status
- ✅ User management

---

## 📊 Architecture Layers

```
Frontend (React)
    ↓
API Client (Axios)
    ↓
Backend Routes (FastAPI)
    ↓
Services (Business Logic)
    ↓
Repositories (Data Access) ⭐ NEW
    ↓
Database (SQLAlchemy)
```

---

## 🎨 Tech Stack

**Backend:** FastAPI, SQLAlchemy, JWT, Alembic  
**Frontend:** React 18, Vite, Tailwind CSS, Lucide Icons  
**Database:** PostgreSQL/SQLite  
**Pattern:** Repository + Service Layer

---

## 📝 Environment Variables

### Backend .env
```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=<generate-new-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DEBUG=True
ALLOWED_ORIGINS=http://localhost:5173
UPLOAD_DIR=uploads
MAX_FILE_SIZE=5242880
```

---

## 🔍 Testing Flow

1. Register user → Login
2. Browse menu → Add to cart
3. Checkout → Place order
4. Admin login → Dashboard
5. Manage menu → Upload image
6. Update order status

---

## 💡 Pro Tips

1. Keep both terminals open while developing
2. Hot reload enabled - changes auto-refresh
3. Use Swagger UI to test APIs directly
4. Check browser console (F12) for errors
5. Admin panel accessible only with admin role

---

## 🆘 Emergency Reset

```bash
# Full reset (WARNING: Deletes all data!)
cd coalspark/backend
del app.db
alembic upgrade head
python create_admin.py

cd ../frontend
rmdir /s /q node_modules
npm install
```

---

## 📞 Need Help?

1. Check HOW_TO_RUN.md for detailed guide
2. Review README.md for full documentation
3. Check IMPLEMENTATION_STATUS.md for features
4. View API docs at http://localhost:8000/docs

---

**Quick Start Success!** 🚀

Both servers running? Open http://localhost:5173 and enjoy!
