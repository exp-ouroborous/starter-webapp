# 🏗️ Scaffold Tool Documentation

The scaffold tool helps you create new projects from the starter-webapp template with customized names, configurations, and automatic setup.

## 🚀 Quick Start

### Interactive Mode (Recommended)
```bash
python scaffold.py
```
The tool will prompt you for:
- Project name
- Project description (optional)

### Command Line Mode
```bash
# Basic usage
python scaffold.py --name my-awesome-app

# With description
python scaffold.py --name blog-platform --description "A modern blogging platform"

# Custom target directory
python scaffold.py --name ecommerce --target ../my-projects/ecommerce

# See all options
python scaffold.py --help
```

## 📋 What the Scaffold Tool Does

### 1. **Project Structure Creation**
- Copies entire template structure to new directory
- Excludes development files (venv, node_modules, .git, etc.)
- Preserves file permissions and timestamps

### 2. **Name Customization**
- Replaces `starter-webapp` with your project name throughout
- Updates package.json files with new project name
- Customizes deployment configurations
- Updates README and documentation

### 3. **Git Repository Setup**
- Initializes new git repository
- Creates comprehensive .gitignore
- Makes initial commit with project information

### 4. **Environment Configuration**
- Creates .env files from templates
- Sets up development configuration
- Prepares production environment templates

### 5. **Dependency Installation** (Optional)
- Creates Python virtual environment
- Installs backend dependencies
- Installs frontend Node.js dependencies

### 6. **Documentation Generation**
- Creates PROJECT_SUMMARY.md with quick start guide
- Updates all documentation with project-specific information
- Provides next steps and development workflow

## 🔧 Command Line Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--name` | `-n` | Project name | `--name my-app` |
| `--description` | `-d` | Project description | `--description "My awesome app"` |
| `--target` | `-t` | Target directory | `--target ../projects/my-app` |
| `--skip-deps` | | Skip dependency installation | `--skip-deps` |
| `--help` | `-h` | Show help message | `--help` |

## 📝 Project Name Rules

### Valid Names
- Must start with a letter
- Can contain lowercase letters, numbers, hyphens, and underscores
- Must be at least 2 characters long
- Examples: `my-app`, `blog_platform`, `ecommerce-site`

### Invalid Names
- Cannot start with numbers or special characters
- Cannot contain uppercase letters or spaces
- Cannot be empty or too short
- Examples: `1app`, `My App`, `app!`, `a`

### Name Sanitization
The tool automatically sanitizes names:
- Converts to lowercase
- Replaces spaces and special characters with hyphens
- Removes consecutive hyphens
- Example: `My Awesome App!` → `my-awesome-app`

## 🎯 Generated Project Structure

```
my-awesome-app/
├── README.md                    # Updated with project name
├── PROJECT_SUMMARY.md           # Quick start guide
├── DEVELOPMENT.md              # Development setup
├── DEPLOYMENT.md               # Production deployment
├── WORKFLOW.md                 # Team workflows
├── .gitignore                  # Comprehensive gitignore
├── backend/
│   ├── .env                    # Development environment
│   ├── venv/                   # Python virtual environment
│   └── ...                     # All backend files
├── frontend/
│   ├── .env                    # Development environment
│   ├── node_modules/           # Node.js dependencies
│   └── ...                     # All frontend files
└── ...
```

## 🔄 Name Replacement Examples

The tool performs intelligent name replacement:

| Template | Generated (project: `blog-platform`) |
|----------|---------------------------------------|
| `starter-webapp` | `blog-platform` |
| `starter_webapp` | `blog_platform` |
| `Starter Web App` | `Blog Platform` |
| `starter-webapp-frontend` | `blog-platform-frontend` |
| `starter-webapp-backend` | `blog-platform-backend` |

## 🚀 After Scaffolding

### Immediate Next Steps
1. **Navigate to project**: `cd my-awesome-app`
2. **Start backend**: `cd backend && python dev.py server`
3. **Start frontend**: `cd frontend && node dev.js server`
4. **Access app**: Visit http://localhost:5173

### Customization
1. **Update README.md** with your specific project details
2. **Modify database models** in `backend/app/db/models.py`
3. **Add React components** in `frontend/src/`
4. **Configure deployment** URLs in environment files

### Development Workflow
1. **Follow WORKFLOW.md** for team development practices
2. **Use helper scripts** (`dev.py`, `dev.js`) for common tasks
3. **Read DEVELOPMENT.md** for detailed setup instructions

## 🛠️ Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x scaffold.py
   python scaffold.py
   ```

2. **Target Directory Exists**
   - Tool will warn if directory is not empty
   - Choose different name or remove existing directory

3. **Dependency Installation Fails**
   - Tool continues even if deps fail
   - Install manually using helper scripts:
   ```bash
   cd backend && python dev.py setup
   cd frontend && node dev.js setup
   ```

4. **Git Not Initialized**
   - Ensure git is installed: `git --version`
   - Initialize manually: `git init && git add . && git commit -m "Initial commit"`

### Manual Setup (If Tool Fails)
```bash
# Copy template manually
cp -r starter-webapp my-new-project
cd my-new-project

# Clean up
rm -rf .git venv node_modules *.db

# Setup manually
cd backend && python dev.py setup
cd frontend && node dev.js setup

# Initialize git
git init && git add . && git commit -m "Initial commit"
```

## 🔍 Advanced Usage

### Custom Template Modifications
Before running scaffold, you can:
1. Modify template files to add your defaults
2. Add additional template files for replacement
3. Customize the scaffold script itself

### Batch Generation
```bash
# Generate multiple projects
python scaffold.py --name project1 --target ./projects/project1
python scaffold.py --name project2 --target ./projects/project2
python scaffold.py --name project3 --target ./projects/project3
```

### CI/CD Integration
```bash
# Use in automation scripts
python scaffold.py \
  --name "$PROJECT_NAME" \
  --description "$PROJECT_DESCRIPTION" \
  --target "$TARGET_DIR" \
  --skip-deps
```

## 📊 Features Summary

- ✅ **Interactive and CLI modes** for flexibility
- ✅ **Intelligent name replacement** throughout all files
- ✅ **Git repository initialization** with proper .gitignore
- ✅ **Environment file setup** for development
- ✅ **Dependency installation** (Python venv + npm)
- ✅ **Comprehensive documentation** generation
- ✅ **Project validation** and sanitization
- ✅ **Cross-platform support** (Windows, Mac, Linux)
- ✅ **Error handling** with helpful messages
- ✅ **Progress feedback** with colored output

## 🎯 Examples

### Simple Project
```bash
python scaffold.py --name todo-app
# Creates: ./todo-app/
```

### Complex Project
```bash
python scaffold.py \
  --name ecommerce-platform \
  --description "A modern e-commerce platform with React and FastAPI" \
  --target ../my-projects/ecommerce
# Creates: ../my-projects/ecommerce/
```

### Blog Platform
```bash
python scaffold.py --name blog-cms --description "Content management system for bloggers"
# Creates: ./blog-cms/
```

---

**🎉 Ready to scaffold?** Run `python scaffold.py` and start building your next amazing project!