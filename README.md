# Full-Stack Web App Starter Template

A complete starter template for building full-stack web applications with:
- **FastAPI** backend with PostgreSQL database support
- **React + Vite** frontend 
- **Render** deployment for backend
- **Cloudflare Pages** deployment for frontend

## Quick Start

### Easy Setup (Recommended)

Use our development helper scripts for a streamlined setup:

1. **Backend Setup** (Terminal 1):
```bash
cd backend
python -m venv venv && source venv/bin/activate  # Create and activate virtual environment
python dev.py setup    # Install dependencies, create .env, setup database
python dev.py server   # Start development server
```

2. **Frontend Setup** (Terminal 2):
```bash
cd frontend
node dev.js setup      # Install dependencies and create .env
node dev.js server     # Start development server
```

3. **Access Application**:
   - Frontend: `http://localhost:5173`
   - Backend API: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

### Alternative Setup

You can also use traditional commands or Makefiles:

```bash
# Using Make (if available)
cd backend && make setup && make server
cd frontend && make setup && make server

# Using npm/pip directly
cd backend && uvicorn app.main:app --reload
cd frontend && npm run dev
```

## Backend Setup

### Initial Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database URL and other settings
```

### Database Setup

**For first-time setup (new project):**
```bash
# Create initial migration from your models
alembic revision --autogenerate -m "Initial migration"

# Apply the migration to create tables
alembic upgrade head
```

**If database already exists (cloning existing project):**
```bash
# Just apply existing migrations
alembic upgrade head
```

### Running the Backend

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Backend Features
- FastAPI with automatic API documentation (`/docs`)
- CORS middleware for frontend integration
- PostgreSQL database support with SQLAlchemy
- Database migrations with Alembic
- Environment-based configuration
- Ready for Render deployment

### Available API Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/hello` - API hello message
- `GET /api/users` - Get all users

### Testing the Backend
```bash
# Test health check
curl http://localhost:8000/health

# Test API endpoint
curl http://localhost:8000/api/hello
```

## Frontend Setup

### Initial Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API URL (default: http://localhost:8000)
```

### Running the Frontend

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Frontend Features
- React with Vite for fast development
- Modern responsive UI components
- API integration with backend
- Environment-based configuration
- Ready for Cloudflare Pages deployment

### Testing Full-Stack Integration

When both servers are running, visit `http://localhost:5173` to see:
- Backend status indicators (API message and health check)
- User data (empty initially, but no errors)
- Modern responsive UI

## Database Management with Alembic

Alembic is a database migration tool that helps you version control your database schema changes. Here's how it works:

### Understanding Alembic

- **Models** (`app/db/models.py`): Define your database structure using SQLAlchemy classes
- **Migrations** (`alembic/versions/`): Python scripts that describe how to change your database
- **Migration History**: Alembic tracks which migrations have been applied to your database

### Common Alembic Workflows

**1. Adding a new model or changing existing models:**
```bash
# After modifying models.py, create a new migration
alembic revision --autogenerate -m "Add new table" 

# Review the generated migration file in alembic/versions/
# Then apply it to your database
alembic upgrade head
```

**2. Checking migration status:**
```bash
# See current migration version
alembic current

# See migration history
alembic history

# See pending migrations
alembic show head
```

**3. Rolling back migrations:**
```bash
# Downgrade to previous migration
alembic downgrade -1

# Downgrade to specific migration
alembic downgrade abc123
```

**4. Database setup scenarios:**

- **New project**: Create initial migration → Apply migration
- **Existing project**: Just apply existing migrations  
- **Production deployment**: Only run `alembic upgrade head`
- **Team collaboration**: Always pull latest migrations before creating new ones

### Important Notes

- Always review auto-generated migrations before applying them
- Test migrations on development data before production
- Backup your database before running migrations in production
- Don't edit migration files after they've been committed to version control


## Project Structure

```
starter-webapp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI application
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py         # Configuration settings
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── database.py       # Database connection
│   │       └── models.py         # SQLAlchemy models
│   ├── alembic/                  # Database migrations
│   ├── requirements.txt          # Python dependencies
│   ├── render.yaml               # Render deployment config
│   └── .env.example              # Environment variables template
└── README.md
```

## Features

### Backend Features
- FastAPI with automatic API documentation
- CORS middleware for frontend integration
- PostgreSQL database support with SQLAlchemy
- Database migrations with Alembic
- Environment-based configuration
- Ready for Render deployment

### Deployment Ready
- ✅ Automated backend deployment to Render
- ✅ Automated frontend deployment to Cloudflare Workers
- ✅ GitHub Actions CI/CD workflows
- ✅ Production-ready database configuration
- ✅ Environment-based configuration management

## Deployment

This application is production-ready with automated deployment configurations for both backend and frontend.

### Quick Deployment

**Automated Setup (Recommended):**
1. Fork this repository
2. Set up backend on Render (see [DEPLOYMENT.md](DEPLOYMENT.md))
3. Set up frontend on Cloudflare Workers (see [DEPLOYMENT.md](DEPLOYMENT.md))
4. Configure GitHub Actions secrets
5. Push to main branch - deployments happen automatically!

**Manual Setup:**
- Backend: Render will auto-deploy from `render.yaml` configuration
- Frontend: Cloudflare Workers will auto-deploy from `wrangler.toml`

### Backend (Render)

**Automatic Configuration:**
- Database setup with PostgreSQL
- Auto-migration on deployment
- Environment variable management
- Health checks and monitoring

**Key Features:**
- `render.yaml` with complete service configuration
- `deploy.py` script for production setup
- Connection pooling for PostgreSQL
- Automatic CORS configuration

### Frontend (Cloudflare Workers)

**Automatic Configuration:**
- Multi-environment support (dev/preview/production)
- Static asset serving with Workers
- SPA routing support for React

**Key Features:**
- `wrangler.toml` with Workers configuration
- Custom worker script for asset handling
- GitHub Actions workflow for CI/CD
- Environment indicators in UI
- Automatic API URL configuration

### CI/CD Workflows

**Automated Deployments:**
- Backend: Triggered on `/backend` changes
- Frontend: Triggered on `/frontend` changes
- Linting and testing in CI pipeline
- Secrets management for production variables

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Development

This project includes comprehensive development tools and helpers for a smooth development experience.

### 🛠️ Development Tools

**Helper Scripts:**
- `backend/dev.py` - Python development helper with commands for setup, server, database operations, linting, etc.
- `frontend/dev.js` - Node.js development helper with commands for setup, server, build, deploy, etc.
- `Makefiles` - Traditional make commands for both backend and frontend

**Available Commands:**
```bash
# Backend
python dev.py setup      # Complete environment setup
python dev.py server     # Start development server
python dev.py db-migrate "message"  # Create database migration
python dev.py lint       # Check code quality
python dev.py format     # Format code

# Frontend  
node dev.js setup        # Complete environment setup
node dev.js server       # Start development server
node dev.js build        # Build for production
node dev.js lint         # Check code quality
node dev.js fix          # Fix formatting issues
```

**Documentation:**
- `DEVELOPMENT.md` - Comprehensive development setup and workflow guide
- Enhanced `.env.example` files with detailed configuration options

### Environment Variables

Both backend and frontend include comprehensive `.env.example` files. Copy and customize:

```bash
# Backend
cp backend/.env.example backend/.env

# Frontend  
cp frontend/.env.example frontend/.env
```

For detailed development instructions, see [DEVELOPMENT.md](DEVELOPMENT.md).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use this template for your projects!