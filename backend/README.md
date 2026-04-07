# 🔥 CoalSpark Restaurant

A modern, full-stack restaurant ordering application with a premium dark-themed UI featuring ember/orange accents. Built with **FastAPI** backend and **React** frontend.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Default Credentials](#default-credentials)
- [API Documentation](#api-documentation)
- [Repository Pattern](#repository-pattern)
- [Screenshots](#screenshots)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Customer Features
- ✅ Browse menu by categories (BBQ, Biryani, Starters, etc.)
- ✅ Search dishes by name/description
- ✅ Shopping cart with quantity management
- ✅ User authentication (login/register)
- ✅ Order placement with delivery address
- ✅ Order history tracking
- ✅ Spice level indicators
- ✅ Veg/Non-veg badges

### Admin Features
- ✅ Dashboard with key metrics
- ✅ Manage menu items (CRUD operations)
- ✅ Upload food images
- ✅ Update order status
- ✅ User management
- ✅ Revenue tracking
- ✅ Real-time order monitoring

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLite (easily switchable to PostgreSQL)
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **Password Hashing**: bcrypt via passlib
- **Architecture**: Repository pattern + Service layer

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router v6
- **State Management**: React Context API
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast

---

## 📁 Project Structure

```
Coolspark Restaurant/
├── coalspark/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── api/routes/       # API endpoints
│   │   │   ├── core/             # Config, security
│   │   │   ├── db/               # Database connection
│   │   │   ├── models/           # SQLAlchemy models
│   │   │   ├── repositories/     # Data access layer ⭐ NEW
│   │   │   ├── schemas/          # Pydantic validation
│   │   │   ├── services/         # Business logic
│   │   │   └── utils/            # Helpers, exceptions
│   │   ├── uploads/              # Food images
│   │   ├── main.py               # FastAPI app entry
│   │   ├── alembic/              # DB migrations
│   │   └── requirements.txt
│   └── frontend/
│       ├── src/
│       │   ├── api/              # API client functions
│       │   ├── components/       # Reusable UI components
│       │   ├── context/          # React contexts
│       │   ├── hooks/            # Custom hooks
│       │   ├── pages/            # Page components
│       │   ├── utils/            # Helper functions
│       │   └── App.jsx           # Root component
│       ├── public/               # Static assets
│       └── package.json
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.9+** (via [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html))
- **Node.js 16+**
- **Conda** (recommended) or venv

### Backend Setup (Using Conda - Recommended)

```bash
cd cbackend

# Create conda environment
conda create -n coalspark python=3.9 -y

# Activate environment
conda activate coalspark

# Install dependencies from environment.yml
conda env create -f environment.yml

# OR install from requirements.txt
pip install -r requirements.txt

# Copy .env.example to .env (if exists) or create .env file
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Seed sample data with images
python seed_data.py

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs on: **http://localhost:8000**

### Alternative: Using venv

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and start server
alembic upgrade head
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on: **http://localhost:5173**

---

## ▶️ Running the Application

### Quick Start (Both Backend & Frontend)

**Terminal 1 - Backend (Conda):**
```bash
cd coalspark/backend
conda activate coalspark
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd coalspark/frontend
npm run dev
```

Open browser: **http://localhost:5173**

---

## 🔐 Default Credentials

### Admin Account
- **Email**: `admin@coalspark.in`
- **Password**: `admin1234`

### Test User Account
- Register a new account via `/register`

---

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

#### Menu
- `GET /api/menu` - Get all menu items
- `GET /api/menu/{id}` - Get single item
- `POST /api/menu` - Create item (admin)
- `PUT /api/menu/{id}` - Update item (admin)
- `DELETE /api/menu/{id}` - Delete item (admin)
- `POST /api/menu/{id}/upload-image` - Upload image (admin)

#### Orders
- `GET /api/orders` - Get my orders
- `POST /api/orders` - Place new order
- `GET /api/orders/{id}` - Get order details

#### Admin
- `GET /api/admin/dashboard` - Dashboard stats
- `GET /api/admin/users` - All users
- `GET /api/admin/orders` - All orders
- `PUT /api/admin/orders/{id}/status` - Update status

---

## 🗂️ Repository Pattern

The backend uses the **Repository Pattern** for clean architecture:

### Layers
1. **Routes** (`api/routes/`) - HTTP request handling
2. **Services** (`services/`) - Business logic
3. **Repositories** (`repositories/`) - Data access ⭐

### Benefits
- ✅ Separation of concerns
- ✅ Easy to test
- ✅ Reusable data access code
- ✅ Clean business logic

### Example Usage

```python
from app.repositories import UserRepository

# In a service function
def get_user_by_email(db, email):
    user_repo = UserRepository(db)
    return user_repo.get_by_email(email)
```

📖 **Full documentation**: See `backend/REPOSITORIES_README.md`

---

## 📸 Screenshots

### Home Page
- Hero section with restaurant branding
- Cuisine categories grid
- Featured menu items
- Restaurant info and hours

### Menu Page
- Category filter pills
- Search functionality
- Food cards with images
- Add to cart controls

### Cart & Checkout
- Cart sidebar
- Quantity management
- Delivery address form
- Order summary

### Admin Dashboard
- Key metrics cards
- Orders by status breakdown
- Quick action links

---

## 👩‍💻 Development

### Adding New Features

1. **Create Model** (`models/`)
2. **Create Schema** (`schemas/`)
3. **Create Repository** (`repositories/`)
4. **Create Service** (`services/`)
5. **Create Route** (`api/routes/`)
6. **Create Frontend API** (`frontend/src/api/`)
7. **Create Page/Component** (`frontend/src/pages/`)

### Code Style

- Backend: Follow PEP 8, use type hints
- Frontend: ESLint rules enforced
- Commit messages: Descriptive and concise

---

## 🐛 Troubleshooting

### Backend won't start

**Error: ModuleNotFoundError**
```bash
# Make sure conda environment is activated
conda activate coalspark
pip install -r requirements.txt
```

**Error: Database connection failed**
```bash
# For SQLite users, check .env has:
DATABASE_URL=sqlite:///./app.db

# For PostgreSQL users:
# 1. Ensure PostgreSQL service is running
# 2. Verify credentials in .env
# 3. Check database exists
```

**Error: Conda not found**
- Install Miniconda from https://docs.conda.io/en/latest/miniconda.html
- Restart terminal after installation
- Run: `conda --version` to verify

### Frontend build errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Database issues

```bash
# Reset database (WARNING: deletes all data)
cd coalspark/backend
conda activate coalspark
rm app.db  # or del app.db on Windows
alembic upgrade head
python seed_data.py
```

### CORS errors

- Ensure backend allows frontend origin in CORS settings
- Check `main.py` CORS middleware configuration
- Verify `.env` file has correct ALLOWED_ORIGINS

### Images not showing

1. Run seed script: `python seed_data.py`
2. Check backend is running on port 8000
3. Verify image URLs load: http://localhost:8000/api/v1/menu
4. Check browser console (F12) for errors

### Conda Environment Issues

```bash
# List all environments
conda env list

# Remove and recreate environment
conda env remove -n coalspark
conda create -n coalspark python=3.9 -y
conda activate coalspark
pip install -r requirements.txt
```

### CORS errors
- Ensure backend allows frontend origin in CORS settings
- Check `main.py` CORS middleware configuration

---

## 📝 Environment Variables

Create `.env` file in `backend/` directory:

```env
# Database
DATABASE_URL=sqlite:///./app.db

# Security
SECRET_KEY=your-secret-key-here-generate-with-secrets.token_urlsafe(32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Upload settings
MAX_FILE_SIZE=5242880  # 5MB in bytes
UPLOAD_DIR=uploads

# Debug mode
DEBUG=true
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is proprietary software. All rights reserved.

---

## 👥 Credits

Developed with 🔥 by the CoalSpark Team

---

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Contact: support@coalspark.in

---

**Enjoy CoalSpark! Where Fire Meets Flavour** 🔥
