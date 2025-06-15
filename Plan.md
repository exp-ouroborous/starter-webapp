# Full-Stack Web App Starter Template

A starter template project that acts like a boilerplate repo to quickly spin up full-stack web apps with:
* FastAPI backend (CORS + DB support like PostgreSQL)
* React frontend (Vite-based)
* Deployment to Backend on Render and Frontend on Cloudflare Pages

## Implementation Plan

### Phase 1: Backend Setup (FastAPI) ✅ COMPLETED
1. ✅ Create `backend/` directory structure
   - `backend/app/` - Main application code
   - `backend/app/main.py` - FastAPI app entry point
   - `backend/app/api/` - API route handlers
   - `backend/app/db/` - Database models and connection
   - `backend/app/core/` - Configuration and settings

2. ✅ Set up FastAPI application
   - Initialize FastAPI app with CORS middleware
   - Create basic health check endpoint
   - Configure environment-based settings

3. ✅ Add database support
   - Set up SQLAlchemy with PostgreSQL support
   - Create database models and schemas
   - Add database connection and session management
   - Include migration support with Alembic

4. ✅ Create deployment configuration
   - `backend/requirements.txt` - Python dependencies
   - `backend/render.yaml` - Render deployment config
   - Environment variable configuration

**Testing Phase 1:**
- Run `uvicorn app.main:app --reload` from backend directory
- Verify API responds at `http://localhost:8000`
- Test health check endpoint: `curl http://localhost:8000/health`
- Check database connection and run test queries
- Verify CORS headers in browser dev tools

### Phase 2: Frontend Setup (React + Vite) ✅ COMPLETED
1. ✅ Create `frontend/` directory structure
   - Initialize Vite React project
   - Set up project structure with `src/` directory
   - Configure build tools and development server

2. ✅ Set up React application
   - Create main App component
   - Add API integration with backend
   - Configure environment variables for API URL
   - Add modern responsive styling

3. ✅ Configure build and deployment
   - `frontend/package.json` - Dependencies and scripts
   - `frontend/vite.config.js` - Vite configuration
   - Environment configuration for different stages
   - Cloudflare Pages deployment settings

**Testing Phase 2:**
- Run `npm run dev` from frontend directory
- Verify React app loads at `http://localhost:5173`
- Test API integration by checking network requests in dev tools
- Verify environment variables are loaded correctly
- Test build process with `npm run build` and preview with `npm run preview`

### Phase 3: Deployment Configuration
1. Backend deployment (Render)
   - Configure `render.yaml` for automatic deployment
   - Set up environment variables
   - Configure database connection

2. Frontend deployment (Cloudflare Pages)
   - Set up build configuration
   - Configure environment variables
   - Create GitHub Actions workflow

**Testing Phase 3:**
- Test local production build: `npm run build && npm run preview`
- Verify backend deploys successfully on Render (check logs)
- Test deployed backend API endpoints via curl or Postman
- Verify frontend builds and deploys on Cloudflare Pages
- Test full-stack integration between deployed frontend and backend
- Check environment variables are correctly set in both deployments

### Phase 4: Development Tools & Documentation
1. Add development configuration
   - Environment templates (`.env.example`)
   - Development scripts and helpers
   - Local development setup instructions

2. Create comprehensive documentation
   - README with setup instructions
   - Deployment guide
   - Development workflow documentation

3. Scaffold tool
   - Script to generate new projects from template
   - Customizable project name and configuration
   - Git initialization and setup

**Testing Phase 4:**
- Follow README setup instructions from scratch in a new directory
- Test all development scripts and commands work as documented
- Verify `.env.example` files contain all necessary variables
- Test scaffold tool (if implemented) by generating a new project
- Run through complete development workflow: setup → develop → build → deploy
- Validate all documentation is accurate and up-to-date

## Directory Structure
```
starter-webapp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── database.py
│   │       └── models.py
│   ├── requirements.txt
│   ├── render.yaml
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── .env.example
├── .github/
│   └── workflows/
│       └── deploy-frontend.yml
├── README.md
└── scaffold.py (optional)
```
