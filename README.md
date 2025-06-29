# Full-Stack Web App Starter Template

A complete starter template for building full-stack web applications with:
- **FastAPI** backend with PostgreSQL database support
- **React + Vite** frontend 
- **Render** deployment for backend
- **Cloudflare Pages** deployment for frontend

## ⚡ Quick Start

```bash
# Backend (Terminal 1)
cd backend
python dev.py setup && python dev.py server

# Frontend (Terminal 2)  
cd frontend
node dev.js setup && node dev.js server
```

**Access your app**: http://localhost:5173 • **API docs**: http://localhost:8000/docs

> **Need detailed setup?** See [DEVELOPMENT.md](DEVELOPMENT.md) for comprehensive instructions.

## 🗄️ API Endpoints

- `GET /health` - Health check
- `GET /api/hello` - API hello message  
- `GET /api/users` - Get all users
- `GET /docs` - Interactive API documentation

> **For detailed development setup, database management, and troubleshooting**, see [DEVELOPMENT.md](DEVELOPMENT.md)


## 📁 Project Structure

```
starter-webapp/
├── README.md                     # This file - project overview
├── DEVELOPMENT.md               # Detailed development setup guide
├── DEPLOYMENT.md                # Production deployment guide
├── WORKFLOW.md                  # Development workflows and team practices
├── SCAFFOLD.md                  # Scaffold tool documentation
├── scaffold.py                  # Tool to generate new projects from template
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

## 📚 Documentation

Our documentation is organized for clarity and efficiency - each file has a specific purpose to avoid duplication:

| File | Purpose | Target Audience | Focus |
|------|---------|----------------|-------|
| **README.md** (this file) | Project overview & quick start | New users, project browsers | First impression, key features |
| [**DEVELOPMENT.md**](DEVELOPMENT.md) | Development setup & troubleshooting | Developers, contributors | Complete dev reference |
| [**DEPLOYMENT.md**](DEPLOYMENT.md) | Production deployment guide | DevOps, deployment teams | Render & Cloudflare setup |
| [**WORKFLOW.md**](WORKFLOW.md) | Team workflows & Git practices | Development teams | Branching, reviews, CI/CD |
| [**SCAFFOLD.md**](SCAFFOLD.md) | Project generation tool | Template users | Creating new projects |

### 🎯 Documentation Strategy
- **Single source of truth**: Each topic covered comprehensively in one place
- **Clear navigation**: Strategic cross-references instead of duplication  
- **Focused content**: 20% reduction in total documentation while maintaining all essential information
- **User journey optimized**: New users start here, developers live in DEVELOPMENT.md

## 🏗️ Creating New Projects

### Scaffold Tool

Use the included scaffold tool to generate new projects from this template:

```bash
# Interactive mode (recommended)
python scaffold.py

# Command line mode
python scaffold.py --name my-awesome-app --description "My awesome application"

# See all options
python scaffold.py --help
```

**What the scaffold tool does:**
- 📁 Copies template structure with your project name
- 🔧 Updates all configurations and documentation
- 🔄 Initializes git repository with initial commit
- 📦 Sets up development environment and dependencies
- 📋 Creates comprehensive project documentation

For detailed scaffold documentation, see [SCAFFOLD.md](SCAFFOLD.md).

## 🤔 Quick FAQ

**Q: How do I add a new API endpoint?**  
A: Add route in `backend/app/api/routes.py`, test at `/docs`

**Q: How do I deploy to production?**  
A: See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions

**Q: Frontend not connecting to backend?**  
A: Check both servers are running and verify `VITE_API_URL` in frontend `.env`

> **More questions?** See comprehensive FAQ and troubleshooting in [DEVELOPMENT.md](DEVELOPMENT.md)

## 🤝 Contributing

1. Fork the repository and create a feature branch
2. Make changes using the development tools
3. Follow the workflow guidelines in [WORKFLOW.md](WORKFLOW.md)
4. Submit a pull request

## 📄 License

MIT License - feel free to use this template for your projects!

---

**🚀 Ready to build?** Start with the [Quick Start](#-quick-start) above!