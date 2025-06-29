# Development Setup Guide

This guide will help you set up the full-stack web application for local development.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - For the FastAPI backend
- **Node.js 18+** - For the React frontend
- **Git** - For version control
- **Make** (optional) - For using Makefiles

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd starter-webapp
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Set up development environment (installs dependencies, creates .env, initializes DB)
python dev.py setup

# Start the development server
python dev.py server
```

The backend will be available at: http://localhost:8000
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 3. Frontend Setup

```bash
cd frontend

# Set up development environment (installs dependencies, creates .env)
node dev.js setup

# Start the development server
node dev.js server
```

The frontend will be available at: http://localhost:5173

## Detailed Setup Instructions

### Backend Development

#### Environment Setup

1. **Virtual Environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   - Copy `.env.example` to `.env`
   - Modify variables as needed for your local setup

4. **Database Setup**:
   ```bash
   # Initialize database with migrations
   alembic upgrade head
   ```

#### Development Commands

Using the helper script:
```bash
python dev.py setup      # Set up everything
python dev.py server     # Start dev server
python dev.py test       # Run tests
python dev.py lint       # Check code quality
python dev.py format     # Format code
python dev.py clean      # Clean up files
python dev.py db-migrate "message"  # Create migration
python dev.py db-upgrade # Apply migrations
python dev.py db-reset   # Reset database (⚠️  deletes data)
```

Using Makefile (if available):
```bash
make setup      # Set up environment
make server     # Start server
make test       # Run tests
make lint       # Check code
make format     # Format code
```

Using npm/pip directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Database Operations

- **Create Migration**: `python dev.py db-migrate "description"`
- **Apply Migrations**: `python dev.py db-upgrade`
- **Reset Database**: `python dev.py db-reset` (⚠️  WARNING: Deletes all data)

### Frontend Development

#### Environment Setup

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Environment Variables**:
   - Copy `.env.example` to `.env`
   - Modify `VITE_API_URL` if your backend runs on a different port

#### Development Commands

Using the helper script:
```bash
node dev.js setup      # Set up everything
node dev.js server     # Start dev server
node dev.js build      # Build for production
node dev.js preview    # Preview production build
node dev.js test       # Run tests
node dev.js lint       # Check code quality
node dev.js fix        # Fix formatting issues
node dev.js clean      # Clean build files
node dev.js analyze    # Analyze bundle size
```

Using Makefile (if available):
```bash
make setup     # Set up environment
make server    # Start server
make build     # Build for production
make lint      # Check code
make fix       # Fix formatting
```

Using npm directly:
```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview build
npm run lint     # Lint code
```

## Development Workflow

### 1. Daily Development

1. **Start Backend**:
   ```bash
   cd backend
   source venv/bin/activate  # Activate virtual environment
   python dev.py server     # Start backend server
   ```

2. **Start Frontend** (in a new terminal):
   ```bash
   cd frontend
   node dev.js server       # Start frontend server
   ```

3. **Open in Browser**: http://localhost:5173

### 2. Making Changes

1. **Backend Changes**:
   - Modify files in `backend/app/`
   - Server auto-reloads on changes
   - For database changes, create migrations

2. **Frontend Changes**:
   - Modify files in `frontend/src/`
   - Browser auto-reloads on changes
   - Use React DevTools for debugging

### 3. Before Committing

1. **Backend**:
   ```bash
   python dev.py lint    # Check code quality
   python dev.py format  # Format code
   python dev.py test    # Run tests
   ```

2. **Frontend**:
   ```bash
   node dev.js lint      # Check code quality
   node dev.js fix       # Fix formatting
   node dev.js test      # Run tests
   ```

## Common Development Tasks

### Adding New API Endpoints

1. Add route in `backend/app/api/routes.py`
2. Test at http://localhost:8000/docs
3. Update frontend to use new endpoint

### Adding Database Models

1. Modify `backend/app/db/models.py`
2. Create migration: `python dev.py db-migrate "add new model"`
3. Apply migration: `python dev.py db-upgrade`

### Adding Frontend Components

1. Create component in `frontend/src/components/`
2. Import and use in your pages
3. Add styling as needed

### Environment Variables

#### Backend (.env)
```bash
DATABASE_URL=sqlite:///./app.db
ENVIRONMENT=development
DEBUG=true
FRONTEND_URL=http://localhost:5173
```

#### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
VITE_ENVIRONMENT=development
```

## Troubleshooting

### Common Issues

1. **Backend won't start**:
   - Check if virtual environment is activated
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check if port 8000 is already in use

2. **Frontend won't connect to backend**:
   - Verify backend is running on http://localhost:8000
   - Check `VITE_API_URL` in frontend `.env`
   - Look for CORS errors in browser console

3. **Database errors**:
   - Reset database: `python dev.py db-reset`
   - Check database migrations: `python dev.py db-upgrade`

4. **Port conflicts**:
   - Backend default: 8000
   - Frontend default: 5173
   - Change ports in respective configuration files

### Comprehensive Troubleshooting

#### Backend Issues

**Backend won't start:**
- Ensure virtual environment is activated: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Check if port 8000 is already in use
- Verify Python version (3.8+)

**Database errors:**
- Reset database: `python dev.py db-reset` (⚠️ deletes all data)
- Check database URL in `.env`
- Run migrations: `python dev.py db-upgrade`
- Verify database file permissions

**Import/Module errors:**
- Ensure you're in the correct directory (`backend/`)
- Check virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

#### Frontend Issues

**Frontend won't start:**
- Install dependencies: `npm install`
- Check if port 5173 is already in use
- Verify Node.js version (18+)
- Clear node modules: `rm -rf node_modules && npm install`

**API connection problems:**
- Verify backend is running on http://localhost:8000
- Check `VITE_API_URL` in frontend `.env`
- Look for CORS errors in browser console
- Test API directly: `curl http://localhost:8000/health`

**Build failures:**
- Clear Vite cache: `rm -rf node_modules/.vite`
- Check for TypeScript errors
- Verify all imports are correct

#### Full-Stack Integration Issues

**CORS errors:**
- Ensure `FRONTEND_URL` is set correctly in backend `.env`
- Check CORS middleware configuration in `backend/app/main.py`
- Verify both servers are running

**Environment variable issues:**
- Frontend: Variables must start with `VITE_`
- Backend: Check `.env` file exists and is properly formatted
- Restart servers after changing environment variables

#### Development Workflow Issues

**Git/Version control:**
- Ensure you're on the correct branch
- Check for uncommitted changes: `git status`
- Pull latest changes: `git pull origin main`

**Dependency conflicts:**
- Backend: Create fresh virtual environment
- Frontend: Delete `node_modules` and reinstall
- Check for version conflicts in requirements/package files

#### Quick Fix Commands

```bash
# Complete backend reset
cd backend
python dev.py clean && python dev.py setup

# Complete frontend reset  
cd frontend
node dev.js clean && node dev.js setup

# Test basic connectivity
curl http://localhost:8000/health
curl http://localhost:8000/api/hello

# Check running processes
lsof -i :8000  # Backend port
lsof -i :5173  # Frontend port
```

### Getting Additional Help

1. **Check logs and error messages** in terminal output
2. **Test API endpoints** directly using curl or Postman
3. **Review browser console** for frontend errors
4. **Check network tab** for failed API requests
5. **Verify environment variables** are loaded correctly
6. **Compare with working setup** if you have one

## Comprehensive FAQ

### Development Questions

**Q: How do I add a new API endpoint?**
A: Add your route in `backend/app/api/routes.py`, test at `/docs`, then update frontend to use it.

**Q: How do I add a new React component?**  
A: Create your component in `frontend/src/components/`, import and use in your pages.

**Q: How do I change the database schema?**
A: Modify `backend/app/db/models.py`, then run `python dev.py db-migrate "description"` and `python dev.py db-upgrade`.

**Q: How do I reset my development database?**
A: Run `python dev.py db-reset` (⚠️ Warning: This deletes all data).

**Q: How do I run tests?**
A: Use `python dev.py test` for backend and `node dev.js test` for frontend.

**Q: How do I check code quality?**
A: Use `python dev.py lint` and `node dev.js lint` to check code style.

**Q: How do I format my code automatically?**
A: Use `python dev.py format` and `node dev.js fix` to auto-format.

### Environment and Configuration

**Q: What environment variables do I need?**
A: Copy `.env.example` to `.env` in both backend and frontend directories and customize as needed.

**Q: How do I use different database configurations?**
A: Update `DATABASE_URL` in `backend/.env` for different databases (SQLite for dev, PostgreSQL for production).

**Q: How do I run on different ports?**
A: Backend: Set `PORT` in `.env` or use `--port` flag. Frontend: Set `VITE_DEV_PORT` in `.env`.

### Workflow and Git

**Q: What's the recommended Git workflow?**
A: See [WORKFLOW.md](WORKFLOW.md) for comprehensive branching and development practices.

**Q: How do I contribute to the project?**
A: Fork the repo, create a feature branch, make changes, test thoroughly, and submit a PR following [WORKFLOW.md](WORKFLOW.md).

**Q: What commit message format should I use?**
A: Follow conventional commits: `type(scope): description` (e.g., `feat: add user authentication`).

### Deployment and Production

**Q: How do I deploy to production?**
A: See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions to Render and Cloudflare.

**Q: How do I prepare for production deployment?**
A: Set environment variables, run migrations, build frontend, and follow the deployment checklist.

**Q: What's different between development and production?**
A: Production uses PostgreSQL, different CORS settings, and optimized builds. Environment variables control these differences.

## Project Structure

See the detailed project structure in [README.md](README.md#-project-structure).

## Next Steps

1. **Add Tests**: Set up testing frameworks for both backend and frontend
2. **Add Logging**: Implement structured logging for debugging
3. **Add Authentication**: Implement user authentication if needed
4. **Add Monitoring**: Set up error tracking and performance monitoring
5. **Optimize Build**: Configure build optimization for production

---

Happy coding! 🚀