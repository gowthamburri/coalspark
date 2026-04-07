<div align="center">

# 🔥 CoalSpark Multi Cuisine Restaurant

### *Where Fire Meets Flavour*

A full-stack, production-ready restaurant web application built with **FastAPI** + **React**.
Premium dark BBQ-style UI serving BBQ, Biryani, Mandi, Chinese & Italian cuisine.

📍 **Gachibowli, Hyderabad**

---

![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5.2-646CFF?style=for-the-badge&logo=vite&logoColor=white)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [API Reference](#-api-reference)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Alembic Migrations](#-alembic-migrations)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

CoalSpark is a **production-level** restaurant ordering platform featuring a blazing-fast FastAPI backend and a sleek dark-themed React frontend. The entire system is built with clean architecture, modular code, JWT authentication, role-based access control, and an Alembic-managed PostgreSQL database.

> Built as a real-world full-stack reference project — every file is production-grade with full comments, proper error handling, and scalable architecture.

---

## ✨ Features

### 👤 Customer Features
| Feature | Description |
|---------|-------------|
| 🏠 **Home Page** | Hero banner, restaurant info, featured menu items, cuisine categories |
| 🍽️ **Browse Menu** | Browse all 6 cuisine categories with search & filters |
| 🔍 **Search & Filter** | Real-time search + category filter with debounce |
| 🛒 **Smart Cart** | Add/remove items, quantity controls, live total calculation |
| 📦 **Place Orders** | Checkout with delivery address, payment method, special instructions |
| 📜 **Order History** | View all past orders with status tracking |
| ❌ **Cancel Orders** | Cancel pending orders before they are confirmed |
| 🔐 **Auth** | Register, login, JWT-based sessions persisted in localStorage |

### 🔧 Admin Features
| Feature | Description |
|---------|-------------|
| 📊 **Dashboard** | Live stats: revenue, orders, customers, top-selling items |
| 🍖 **Menu CRUD** | Add, edit, delete menu items with image upload |
| 📸 **Image Upload** | Upload JPEG/PNG/WebP food photos (UUID filenames, 5MB limit) |
| 📋 **Order Management** | View all orders, update status (pending → confirmed → preparing → ready → delivered) |
| 👥 **User Management** | View all users, activate/deactivate accounts |
| 🏪 **Restaurant Profile** | Update name, hours, contact info, toggle open/closed |

---

## 🛠 Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.111 | Web framework — async, auto-docs, dependency injection |
| **PostgreSQL** | 16 | Primary relational database |
| **SQLAlchemy** | 2.0 | ORM with declarative models and relationships |
| **Alembic** | 1.13 | Database migrations (autogenerate from models) |
| **python-jose** | 3.3 | JWT token creation and verification (HS256) |
| **passlib[bcrypt]** | 1.7 | Password hashing with bcrypt |
| **pydantic-settings** | 2.2 | Environment variable management with type validation |
| **uvicorn** | 0.29 | ASGI server with hot-reload for development |
| **python-multipart** | 0.0.9 | Multipart form data for image uploads |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.2 | UI library with hooks |
| **Vite** | 5.2 | Build tool with dev server and proxy |
| **Tailwind CSS** | 3.4 | Utility-first CSS with custom CoalSpark dark theme |
| **React Router** | 6.22 | Client-side routing with protected routes |
| **Axios** | 1.6 | HTTP client with JWT interceptors |
| **Context API** | — | Global state for Auth and Cart |
| **React Hot Toast** | 2.4 | Toast notifications |
| **Lucide React** | 0.363 | Icon library |
| **Poppins** | — | Google Font (300–800 weights) |

---

## 📁 Project Structure

```
coalspark/
│
├── backend/                          # FastAPI Python backend
│   ├── alembic/                      # Database migration engine
│   │   ├── versions/                 # Auto-generated migration files
│   │   ├── env.py                    # Alembic environment config
│   │   └── script.py.mako            # Migration file template
│   │
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py             # Pydantic settings (reads .env)
│   │   │   └── security.py           # JWT creation/verification + bcrypt
│   │   │
│   │   ├── db/
│   │   │   ├── base.py               # Imports all models (for Alembic autogenerate)
│   │   │   └── session.py            # Engine, SessionLocal, get_db() dependency
│   │   │
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   │   ├── user.py               # User (id, email, role, hashed_password)
│   │   │   ├── restaurant.py         # Restaurant profile
│   │   │   ├── menu_item.py          # MenuItem (6 categories, spice, veg flag)
│   │   │   ├── order.py              # Order (status lifecycle, total)
│   │   │   └── order_item.py         # OrderItem (price snapshot at order time)
│   │   │
│   │   ├── schemas/                  # Pydantic request/response models
│   │   │   ├── user.py               # UserCreate, UserRead, Token
│   │   │   ├── menu_item.py          # MenuItemCreate, MenuItemRead, MenuItemUpdate
│   │   │   ├── order.py              # OrderCreate, OrderRead, OrderStatusUpdate
│   │   │   └── restaurant.py         # RestaurantRead, RestaurantUpdate
│   │   │
│   │   ├── api/routes/               # HTTP route handlers (thin layer)
│   │   │   ├── auth.py               # POST /register, POST /login, GET /me
│   │   │   ├── menu.py               # GET/POST/PUT/DELETE /menu + image upload
│   │   │   ├── orders.py             # POST/GET /orders, DELETE (cancel)
│   │   │   ├── admin.py              # Dashboard, all orders, user management
│   │   │   └── restaurant.py         # Restaurant profile + open/close toggle
│   │   │
│   │   ├── services/                 # Business logic layer
│   │   │   ├── auth_service.py       # Register, authenticate, generate token
│   │   │   ├── menu_service.py       # CRUD, filtering, image upload logic
│   │   │   ├── order_service.py      # Atomic order creation, status updates
│   │   │   └── admin_service.py      # Dashboard stats, user management
│   │   │
│   │   └── utils/
│   │       ├── dependencies.py       # get_current_user, require_admin, get_optional_user
│   │       └── exceptions.py         # HTTP exception factories (400–500)
│   │
│   ├── uploads/                      # Food images (served as static files)
│   ├── main.py                       # FastAPI app, CORS, routers, static mount
│   ├── alembic.ini                   # Alembic configuration
│   ├── requirements.txt
│   └── .env                          # Environment variables (not committed)
│
└── frontend/                         # React + Vite frontend
    ├── src/
    │   ├── api/                      # Axios API call modules
    │   │   ├── axiosInstance.js      # Base URL, JWT interceptor, 401 handler
    │   │   ├── authApi.js
    │   │   ├── menuApi.js
    │   │   ├── orderApi.js
    │   │   └── adminApi.js
    │   │
    │   ├── context/
    │   │   ├── AuthContext.jsx       # User/token state, login/logout, persistence
    │   │   └── CartContext.jsx       # Cart items, add/remove/clear, sessionStorage
    │   │
    │   ├── components/
    │   │   ├── Navbar.jsx            # Responsive nav with cart badge & user menu
    │   │   ├── FoodCard.jsx          # Menu item card with cart controls
    │   │   ├── CategoryFilter.jsx    # Horizontal pill filter bar
    │   │   ├── CartSidebar.jsx       # Slide-in cart drawer
    │   │   ├── OrderSummary.jsx      # Order history card with status badge
    │   │   └── ProtectedRoute.jsx    # Auth guard + Admin guard HOCs
    │   │
    │   ├── pages/
    │   │   ├── Home.jsx              # Hero, cuisine categories, featured items
    │   │   ├── Menu.jsx              # Full menu with search + filter
    │   │   ├── Cart.jsx              # Checkout page
    │   │   ├── Orders.jsx            # Order history
    │   │   ├── Login.jsx
    │   │   ├── Register.jsx
    │   │   └── admin/
    │   │       ├── AdminLayout.jsx   # Sidebar layout for admin pages
    │   │       ├── AdminDashboard.jsx
    │   │       ├── ManageMenu.jsx    # Full CRUD table with modal form
    │   │       └── ManageOrders.jsx  # Orders table with inline status update
    │   │
    │   ├── hooks/
    │   │   ├── useAuth.js
    │   │   └── useCart.js
    │   │
    │   ├── utils/
    │   │   └── formatCurrency.js     # INR formatter + date formatter
    │   │
    │   ├── App.jsx                   # Router, providers, Toaster
    │   ├── main.jsx
    │   └── index.css                 # Tailwind directives + custom CSS vars
    │
    ├── tailwind.config.js            # Custom colors (coal, ember), animations
    ├── vite.config.js                # Dev proxy to backend
    └── package.json
```

---

## 🗄 Database Schema

```
┌─────────────────────────────────────────────────────────────────────┐
│                         COALSPARK DATABASE                          │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────────┐        ┌─────────────────┐
│    users     │         │   restaurants    │        │   menu_items    │
├──────────────┤         ├──────────────────┤        ├─────────────────┤
│ id (PK)      │         │ id (PK)          │        │ id (PK)         │
│ full_name    │         │ name             │        │ restaurant_id   │◄─┐
│ email UNIQUE │         │ tagline          │───────►│ name            │  │
│ hashed_pw    │         │ description      │        │ description     │  │
│ phone        │         │ address          │        │ price           │  │
│ role (enum)  │         │ city             │        │ category (enum) │  │
│ is_active    │         │ phone            │        │ image_url       │  │
│ created_at   │         │ rating           │        │ is_vegetarian   │  FK
│ updated_at   │         │ total_reviews    │        │ is_available    │  │
└──────┬───────┘         │ opening_time     │        │ is_featured     │  │
       │                 │ closing_time     │        │ spice_level     │  │
       │ 1               │ cuisine_types    │        │ preparation_time│  │
       │                 │ is_open          │        │ created_at      │  │
       ▼                 │ created_at       │        └────────┬────────┘  │
┌──────────────┐         └──────────────────┘                │           │
│    orders    │                                              │ 1:N       │
├──────────────┤                                             ▼           │
│ id (PK)      │◄──────────────────────────────── ┌──────────────────┐  │
│ user_id (FK) │  1:N                              │   order_items    │  │
│ status (enum)│                                   ├──────────────────┤  │
│ total_amount │                                   │ id (PK)          │  │
│ delivery_addr│                                   │ order_id (FK)    │  │
│ special_inst │                                   │ menu_item_id(FK) │──┘
│ payment_mthd │                                   │ quantity         │
│ is_paid      │                                   │ unit_price ◄─ snapshot
│ created_at   │                                   │ subtotal         │
│ updated_at   │                                   └──────────────────┘
└──────────────┘

Enums:
  UserRole    → user | admin
  MenuCategory→ BBQ | Biryani & Mandi | Starters | Main Course | Beverages | Desserts
  OrderStatus → pending | confirmed | preparing | ready | delivered | cancelled
```

---

## 📡 API Reference

All routes prefixed with `/api/v1`. Interactive docs at `http://localhost:8000/docs`.

### 🔐 Authentication
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/register` | ❌ | Register new account, returns JWT |
| `POST` | `/auth/login` | ❌ | Login, returns JWT |
| `GET` | `/auth/me` | ✅ | Get current user profile |
| `PUT` | `/auth/me` | ✅ | Update name / phone |

### 🍽️ Menu
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/menu/` | ❌ | List available items (filter: `?category=BBQ&search=chicken`) |
| `GET` | `/menu/categories` | ❌ | List all category names |
| `GET` | `/menu/{id}` | ❌ | Get single item |
| `POST` | `/menu/` | 🔑 Admin | Create menu item |
| `PUT` | `/menu/{id}` | 🔑 Admin | Partial update |
| `DELETE` | `/menu/{id}` | 🔑 Admin | Delete item + image |
| `POST` | `/menu/{id}/image` | 🔑 Admin | Upload food photo |

### 📦 Orders
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/orders/` | ✅ | Place a new order |
| `GET` | `/orders/me` | ✅ | My order history |
| `GET` | `/orders/{id}` | ✅ | Get single order (own orders only) |
| `DELETE` | `/orders/{id}` | ✅ | Cancel pending order |

### 🔧 Admin
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/admin/dashboard` | 🔑 Admin | Stats, revenue, top items |
| `GET` | `/admin/orders` | 🔑 Admin | All orders |
| `GET` | `/admin/orders/{id}` | 🔑 Admin | Any order detail |
| `PATCH` | `/admin/orders/{id}/status` | 🔑 Admin | Update order status |
| `GET` | `/admin/users` | 🔑 Admin | All users |
| `GET` | `/admin/users/{id}` | 🔑 Admin | Single user |
| `PATCH` | `/admin/users/{id}/toggle` | 🔑 Admin | Activate / deactivate |
| `GET` | `/admin/menu` | 🔑 Admin | All items incl. unavailable |

### 🏪 Restaurant
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/restaurant/` | ❌ | Restaurant profile (auto-seeds) |
| `GET` | `/restaurant/status` | ❌ | Quick open/closed check |
| `PUT` | `/restaurant/` | 🔑 Admin | Update profile |
| `PATCH` | `/restaurant/toggle` | 🔑 Admin | Toggle open/closed |

---

## 🚀 Getting Started

### Prerequisites
- **Python** 3.11+
- **Node.js** 18+
- **PostgreSQL** 14+ (running locally or via Docker)
- **Git**

---

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/coalspark.git
cd coalspark
```

---

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

```bash
# Copy the template
cp .env .env.local

# Edit with your values
nano .env
```

See [Environment Variables](#-environment-variables) for all options.

---

### 4. Create PostgreSQL Database

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create the database
CREATE DATABASE coalspark;

-- Exit
\q
```

---

### 5. Run Database Migrations

```bash
# Inside backend/ with venv activated

# Generate the initial migration from your models
alembic revision --autogenerate -m "initial schema"

# Apply to database
alembic upgrade head
```

---

### 6. Start the Backend

```bash
# Development (with auto-reload)
uvicorn main:app --reload --port 8000

# Or directly
python main.py
```

✅ Backend running at: `http://localhost:8000`
📖 API Docs (Swagger UI): `http://localhost:8000/docs`
📖 API Docs (ReDoc): `http://localhost:8000/redoc`

---

### 7. Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at: `http://localhost:5173`

> The Vite dev server automatically proxies `/api/*` and `/uploads/*` requests to the backend at `localhost:8000`.

---

### 8. Create Your First Admin Account

```bash
# 1. Register a normal account via the UI or API:
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Admin User","email":"admin@coalspark.in","password":"admin1234"}'

# 2. Promote to admin in the database:
psql -U postgres -d coalspark -c \
  "UPDATE users SET role = 'admin' WHERE email = 'admin@coalspark.in';"

# 3. Login via the UI with your admin credentials
```

---

## ⚙️ Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# ── Database ─────────────────────────────────────────────────
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/coalspark

# ── JWT Security ─────────────────────────────────────────────
# Generate a strong key: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-super-secret-key-minimum-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# ── Application ───────────────────────────────────────────────
APP_NAME=CoalSpark Restaurant
APP_VERSION=1.0.0
DEBUG=True

# ── CORS ─────────────────────────────────────────────────────
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# ── File Upload ───────────────────────────────────────────────
UPLOAD_DIR=uploads
MAX_FILE_SIZE=5242880
```

> ⚠️ **Never commit `.env` to version control.** It is already listed in `.gitignore`.

---

## 🗃 Alembic Migrations

```bash
# Navigate to backend with venv activated
cd backend

# Initialize Alembic (already done — skip if cloning)
alembic init alembic

# Create a new migration after changing models
alembic revision --autogenerate -m "describe your change"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history --verbose

# View current DB state
alembic current
```

> **How it works:** `alembic/env.py` imports all models via `app/db/base.py` and connects to the DB using `DATABASE_URL` from `.env`. The `--autogenerate` flag compares your SQLAlchemy models to the live DB schema and generates the necessary `upgrade()` and `downgrade()` functions automatically.

---

## 🎨 UI Theme

The frontend uses a custom **dark BBQ-style** Tailwind theme:

```js
// Custom colors in tailwind.config.js
colors: {
  coal:  { 900: '#0f0f0f', 800: '#1a1a1a' },   // Backgrounds
  ember: { 500: '#ff6b00', 600: '#ea580c' },     // Primary accent (orange)
  ash:   { 100: '#2a2a2a', 200: '#222222' },     // Card surfaces
}

// Custom animations
'fade-in':       'fadeIn 0.4s ease-out',
'slide-up':      'slideUp 0.4s ease-out',
'slide-in-right':'slideInRight 0.35s ease-out',
'pulse-ember':   'pulseEmber 2s ease-in-out infinite',
```

**Font:** Poppins (300, 400, 500, 600, 700, 800) from Google Fonts.

---

## 📦 Build for Production

### Backend
```bash
# Set DEBUG=False in .env
# Run with multiple workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend
```bash
cd frontend
npm run build
# Output: frontend/dist/
```

Serve the `dist/` folder from any static file server (Nginx, Caddy, Vercel, etc.)

---

## 🐳 Docker (Optional)

```bash
# Build and start both services
docker-compose up --build

# Run migrations inside the container
docker-compose exec backend alembic upgrade head
```

---

## 📂 Key Design Patterns

### Backend Architecture
```
HTTP Request
    ↓
API Route (routes/*.py)     ← thin, only HTTP concerns
    ↓
Service Layer (*_service.py) ← all business logic lives here
    ↓
SQLAlchemy ORM (models/)    ← DB access only through models
    ↓
PostgreSQL
```

### Security Model
- **Passwords** — never stored in plaintext; bcrypt hashed with automatic salting
- **Tokens** — HS256 signed JWTs; expiry enforced on every request
- **Role checks** — `require_admin` dependency applied at route registration, not inside handlers
- **IDOR protection** — user orders filtered by both `order.id` AND `order.user_id`
- **Image uploads** — UUID filenames, MIME allowlist, size limit enforced server-side
- **Email enumeration** — same error message for "user not found" and "wrong password"

### Frontend State
```
AuthContext  → user, token, login(), logout(), isAdmin
CartContext  → items[], addItem(), removeItem(), totalPrice
    ↓
Custom Hooks (useAuth, useCart) → clean consumer API
    ↓
API Layer (Axios) → JWT interceptor auto-attaches token, 401 → auto-logout
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes with clear, commented code
4. Run linting: `cd frontend && npm run lint`
5. Test your endpoints in Swagger: `http://localhost:8000/docs`
6. Commit with a clear message: `git commit -m "feat: add table reservation system"`
7. Push and open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Built with 🔥 for CoalSpark Restaurant, Gachibowli, Hyderabad.

---

<div align="center">

**⭐ If this project helped you, please give it a star! ⭐**

*Made with FastAPI + React + ❤️*

</div>
