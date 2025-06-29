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


## 📁 Project Structure

```
starter-webapp/
├── README.md                     # This file - project overview
├── DEVELOPMENT.md               # Detailed development setup guide
├── DEPLOYMENT.md                # Production deployment guide
├── Plan.md                      # Implementation plan and roadmap
├── backend/                     # FastAPI backend
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── api/                 # API routes and endpoints
│   │   ├── core/                # Configuration and settings
│   │   └── db/                  # Database models and connection
│   ├── alembic/                 # Database migrations
│   ├── dev.py                   # Development helper script
│   ├── Makefile                 # Development commands
│   ├── requirements.txt         # Python dependencies
│   ├── render.yaml              # Render deployment config
│   └── .env.example             # Environment variables template
├── frontend/                    # React frontend
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── main.jsx             # React entry point
│   │   ├── assets/              # Static assets
│   │   └── worker.js            # Cloudflare Worker script
│   ├── public/                  # Public assets
│   ├── dist/                    # Built application (generated)
│   ├── dev.js                   # Development helper script
│   ├── Makefile                 # Development commands
│   ├── package.json             # Node.js dependencies and scripts
│   ├── vite.config.js           # Vite build configuration
│   ├── wrangler.toml            # Cloudflare Workers config
│   └── .env.example             # Environment variables template
├── .github/
│   └── workflows/               # GitHub Actions CI/CD
└── scripts/                     # Utility scripts
```

## ✨ Features

### 🚀 Backend Features
- **FastAPI** with automatic API documentation (`/docs`)
- **CORS middleware** for secure frontend integration
- **PostgreSQL** database support with SQLAlchemy ORM
- **Database migrations** with Alembic for version control
- **Environment-based configuration** for development/production
- **Health checks** and monitoring endpoints
- **Development tools** with helper scripts and Makefiles

### 🎨 Frontend Features
- **React 19** with modern hooks and features
- **Vite** for fast development and optimized builds
- **Responsive design** with modern CSS
- **Environment indicators** showing deployment status
- **API integration** with backend health monitoring
- **SPA routing** support for client-side navigation
- **Development tools** with helper scripts and hot reload

### 🔧 Development Tools
- **One-command setup** for both backend and frontend
- **Development helper scripts** (`dev.py`, `dev.js`)
- **Makefiles** for traditional development workflows
- **Comprehensive documentation** (setup, development, deployment)
- **Environment templates** with detailed configuration options
- **Code formatting** and linting tools integration
- **Database management** commands for migrations and resets

### 🌐 Deployment Ready
- ✅ **Automated backend deployment** to Render with PostgreSQL
- ✅ **Automated frontend deployment** to Cloudflare Workers
- ✅ **GitHub Actions CI/CD** workflows with automated testing
- ✅ **Production-ready database** configuration with connection pooling
- ✅ **Environment-based configuration** management
- ✅ **Multi-environment support** (development, preview, production)
- ✅ **Security headers** and CORS configuration
- ✅ **Monitoring and logging** setup

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

## 🤔 FAQ

### Common Questions

**Q: How do I add a new API endpoint?**
A: Add your route in `backend/app/api/routes.py`, test at `/docs`, then update frontend to use it.

**Q: How do I add a new React component?**  
A: Create your component in `frontend/src/components/`, import and use in your pages.

**Q: How do I change the database schema?**
A: Modify `backend/app/db/models.py`, then run `python dev.py db-migrate "description"` and `python dev.py db-upgrade`.

**Q: How do I deploy to production?**
A: See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions to Render and Cloudflare.

**Q: How do I reset my development database?**
A: Run `python dev.py db-reset` (⚠️ Warning: This deletes all data).

**Q: Why is my frontend not connecting to the backend?**
A: Check that both servers are running, verify `VITE_API_URL` in frontend `.env`, and check for CORS errors in browser console.

### Troubleshooting

**Backend won't start:**
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Check if port 8000 is in use

**Frontend won't start:**
- Install dependencies: `npm install`
- Check if port 5173 is in use
- Verify Node.js version (18+)

**Database errors:**
- Reset database: `python dev.py db-reset`
- Check database URL in `.env`
- Run migrations: `python dev.py db-upgrade`

## 🆘 Getting Help

1. **Check Documentation**:
   - [DEVELOPMENT.md](DEVELOPMENT.md) - Development setup and workflow
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment guide
   - API docs at `http://localhost:8000/docs` when backend is running

2. **Check Logs**:
   - Backend: Terminal output when running `python dev.py server`
   - Frontend: Browser console for client-side errors
   - Network tab for API request/response debugging

3. **Test Endpoints**:
   - Health check: `curl http://localhost:8000/health`
   - API test: `curl http://localhost:8000/api/hello`

4. **Common Fix Commands**:
   ```bash
   # Backend issues
   cd backend
   python dev.py clean      # Clean up
   python dev.py setup      # Reinstall everything
   
   # Frontend issues  
   cd frontend
   node dev.js clean        # Clean build files
   node dev.js setup        # Reinstall everything
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly using the development tools
5. Commit with clear message (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Submit a pull request

### Development Workflow

1. **Setup**: Use `python dev.py setup` and `node dev.js setup`
2. **Code**: Make changes with hot reload enabled
3. **Test**: Run `python dev.py test` and `node dev.js test`
4. **Quality**: Run `python dev.py lint` and `node dev.js lint`
5. **Commit**: Follow conventional commit messages

## 📄 License

MIT License - feel free to use this template for your projects!

---

## 🎯 Next Steps

After setting up the project, consider:

1. **Add Authentication**: Implement user login/registration
2. **Add Testing**: Set up comprehensive test suites
3. **Add Monitoring**: Integrate error tracking (Sentry) and analytics
4. **Add Features**: Build your specific application features
5. **Optimize**: Performance tune for your use case
6. **Scale**: Consider caching, CDN, and database optimization

**Happy coding!** 🚀