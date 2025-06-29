#!/usr/bin/env python3
"""
Scaffold Tool for Full-Stack Web App Starter Template

This script generates new projects from the starter template with customizable
project names, configurations, and automatic setup.

Usage:
    python scaffold.py
    python scaffold.py --name my-app --description "My awesome app"
    python scaffold.py --help
"""

import os
import sys
import shutil
import argparse
import subprocess
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

# Colors for console output
class Colors:
    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'

def log(message: str, color: str = Colors.RESET) -> None:
    """Print colored log message"""
    print(f"{color}{message}{Colors.RESET}")

def run_command(command: str, cwd: Optional[str] = None, check: bool = True) -> bool:
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=check,
            capture_output=True, 
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        log(f"❌ Command failed: {command}", Colors.RED)
        if e.stdout:
            log(f"STDOUT: {e.stdout}", Colors.YELLOW)
        if e.stderr:
            log(f"STDERR: {e.stderr}", Colors.YELLOW)
        return False

def validate_project_name(name: str) -> bool:
    """Validate project name follows conventions"""
    # Must be lowercase, can contain hyphens and underscores
    pattern = r'^[a-z][a-z0-9\-_]*[a-z0-9]$'
    return bool(re.match(pattern, name)) and len(name) >= 2

def sanitize_name(name: str) -> str:
    """Convert name to valid project name format"""
    # Convert to lowercase, replace spaces and special chars with hyphens
    sanitized = re.sub(r'[^a-z0-9\-_]', '-', name.lower())
    # Remove multiple consecutive hyphens
    sanitized = re.sub(r'-+', '-', sanitized)
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-_')
    return sanitized

class ProjectScaffolder:
    """Main scaffolding class"""
    
    def __init__(self, project_name: str, description: str, target_dir: str):
        self.project_name = project_name
        self.description = description
        self.target_dir = Path(target_dir).resolve()
        self.template_dir = Path(__file__).parent.resolve()
        
        # Derived names
        self.snake_case_name = project_name.replace('-', '_')
        self.title_case_name = project_name.replace('-', ' ').replace('_', ' ').title()
        self.camel_case_name = ''.join(word.capitalize() for word in project_name.replace('-', '_').split('_'))
        
        # Files and directories to exclude from copying
        self.exclude_patterns = {
            '__pycache__',
            '*.pyc',
            '*.pyo',
            '.git',
            '.gitignore',
            'venv',
            'node_modules',
            '.env',
            '*.db',
            'dist',
            '.vite',
            'temp.tmp',
            'scaffold.py',  # Don't copy the scaffold script itself
        }
        
        # Files that need content replacement
        self.template_files = [
            'README.md',
            'package.json',
            'backend/requirements.txt',
            'backend/render.yaml',
            'frontend/package.json',
            'frontend/wrangler.toml',
            'frontend/index.html',
            'frontend/src/App.jsx',
            'backend/.env.example',
            'frontend/.env.example',
        ]

    def should_exclude(self, path: Path) -> bool:
        """Check if a file/directory should be excluded"""
        for pattern in self.exclude_patterns:
            if pattern.startswith('*'):
                if path.name.endswith(pattern[1:]):
                    return True
            elif path.name == pattern:
                return True
        return False

    def copy_template_structure(self) -> bool:
        """Copy the template directory structure to target location"""
        log(f"📁 Copying template structure to {self.target_dir}", Colors.BLUE)
        
        try:
            for root, dirs, files in os.walk(self.template_dir):
                # Remove excluded directories from dirs list (modifies in-place)
                dirs[:] = [d for d in dirs if not self.should_exclude(Path(root) / d)]
                
                for file in files:
                    src_path = Path(root) / file
                    
                    # Skip excluded files
                    if self.should_exclude(src_path):
                        continue
                    
                    # Calculate relative path from template root
                    rel_path = src_path.relative_to(self.template_dir)
                    dest_path = self.target_dir / rel_path
                    
                    # Create directory if it doesn't exist
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(src_path, dest_path)
            
            log("✅ Template structure copied successfully", Colors.GREEN)
            return True
            
        except Exception as e:
            log(f"❌ Failed to copy template structure: {e}", Colors.RED)
            return False

    def update_file_contents(self) -> bool:
        """Update template files with project-specific content"""
        log("📝 Updating file contents with project information", Colors.BLUE)
        
        replacements = {
            'starter-webapp': self.project_name,
            'starter_webapp': self.snake_case_name,
            'Starter Web App': self.title_case_name,
            'Full-stack template with FastAPI + React': self.description,
            'starter-webapp-frontend': f"{self.project_name}-frontend",
            'starter-webapp-backend': f"{self.project_name}-backend",
            'starter-webapp-db': f"{self.project_name}-db",
        }
        
        try:
            for template_file in self.template_files:
                file_path = self.target_dir / template_file
                
                if not file_path.exists():
                    continue
                
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Apply replacements
                for old, new in replacements.items():
                    content = content.replace(old, new)
                
                # Write updated content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            log("✅ File contents updated successfully", Colors.GREEN)
            return True
            
        except Exception as e:
            log(f"❌ Failed to update file contents: {e}", Colors.RED)
            return False

    def initialize_git_repository(self) -> bool:
        """Initialize git repository and create initial commit"""
        log("🔧 Initializing git repository", Colors.BLUE)
        
        try:
            # Initialize git repo
            if not run_command("git init", cwd=self.target_dir):
                return False
            
            # Create .gitignore
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
ENV/
env/
.venv

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Database
*.db
*.sqlite3

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*
.pnpm-debug.log*

# Build outputs
dist/
build/
.vite/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs
*.log

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# Temporary files
*.tmp
temp.tmp
"""
            
            with open(self.target_dir / '.gitignore', 'w') as f:
                f.write(gitignore_content)
            
            # Add all files
            if not run_command("git add .", cwd=self.target_dir):
                return False
            
            # Create initial commit
            commit_message = f"Initial commit: {self.title_case_name}\n\nGenerated from starter-webapp template\n\n🤖 Generated with scaffold tool"
            if not run_command(f'git commit -m "{commit_message}"', cwd=self.target_dir):
                return False
            
            log("✅ Git repository initialized with initial commit", Colors.GREEN)
            return True
            
        except Exception as e:
            log(f"❌ Failed to initialize git repository: {e}", Colors.RED)
            return False

    def setup_development_environment(self) -> bool:
        """Set up development environment with dependencies"""
        log("🔧 Setting up development environment", Colors.BLUE)
        
        try:
            # Create backend .env file
            backend_env_path = self.target_dir / 'backend' / '.env'
            backend_env_example = self.target_dir / 'backend' / '.env.example'
            if backend_env_example.exists():
                shutil.copy2(backend_env_example, backend_env_path)
                log("📄 Created backend/.env from template", Colors.GREEN)
            
            # Create frontend .env file
            frontend_env_path = self.target_dir / 'frontend' / '.env'
            frontend_env_example = self.target_dir / 'frontend' / '.env.example'
            if frontend_env_example.exists():
                shutil.copy2(frontend_env_example, frontend_env_path)
                log("📄 Created frontend/.env from template", Colors.GREEN)
            
            # Try to install dependencies (optional)
            log("📦 Installing dependencies (this may take a while)...", Colors.YELLOW)
            
            # Backend dependencies
            backend_dir = self.target_dir / 'backend'
            if (backend_dir / 'requirements.txt').exists():
                log("📦 Installing Python dependencies...", Colors.BLUE)
                venv_success = run_command("python -m venv venv", cwd=backend_dir, check=False)
                if venv_success:
                    # Activate venv and install
                    if sys.platform == "win32":
                        activate_cmd = "venv\\Scripts\\activate && pip install --upgrade pip && pip install -r requirements.txt"
                    else:
                        activate_cmd = "source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"
                    
                    if run_command(activate_cmd, cwd=backend_dir, check=False):
                        log("✅ Backend dependencies installed", Colors.GREEN)
                    else:
                        log("⚠️  Backend dependency installation failed (run manually)", Colors.YELLOW)
                else:
                    log("⚠️  Virtual environment creation failed", Colors.YELLOW)
            
            # Frontend dependencies
            frontend_dir = self.target_dir / 'frontend'
            if (frontend_dir / 'package.json').exists():
                log("📦 Installing Node.js dependencies...", Colors.BLUE)
                if run_command("npm install", cwd=frontend_dir, check=False):
                    log("✅ Frontend dependencies installed", Colors.GREEN)
                else:
                    log("⚠️  Frontend dependency installation failed (run manually)", Colors.YELLOW)
            
            return True
            
        except Exception as e:
            log(f"❌ Failed to set up development environment: {e}", Colors.RED)
            return False

    def create_project_summary(self) -> None:
        """Create a summary file with project information"""
        summary_content = f"""# {self.title_case_name}

{self.description}

## Project Information

- **Name**: {self.project_name}
- **Description**: {self.description}
- **Generated**: {subprocess.check_output(['date'], text=True).strip()}
- **Template**: starter-webapp

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
python dev.py setup
python dev.py server
```

### Frontend Setup
```bash
cd frontend
node dev.js setup
node dev.js server
```

### Access Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Next Steps

1. **Review Documentation**:
   - [README.md](README.md) - Project overview and setup
   - [DEVELOPMENT.md](DEVELOPMENT.md) - Development workflow
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
   - [WORKFLOW.md](WORKFLOW.md) - Team workflows

2. **Customize Your App**:
   - Update project description in README.md
   - Modify database models in `backend/app/db/models.py`
   - Add your React components in `frontend/src/`
   - Configure deployment URLs in environment files

3. **Development Workflow**:
   - Follow branching strategy in WORKFLOW.md
   - Use development helper scripts (dev.py, dev.js)
   - Run quality checks before committing

4. **Deploy to Production**:
   - Set up Render account for backend
   - Set up Cloudflare account for frontend
   - Follow DEPLOYMENT.md guide

## Support

- Check documentation files for detailed guides
- Review FAQ in README.md for common issues
- Use development helper scripts for common tasks

Happy coding! 🚀
"""
        
        try:
            with open(self.target_dir / 'PROJECT_SUMMARY.md', 'w') as f:
                f.write(summary_content)
            log("📄 Created PROJECT_SUMMARY.md", Colors.GREEN)
        except Exception as e:
            log(f"⚠️  Could not create project summary: {e}", Colors.YELLOW)

    def scaffold(self) -> bool:
        """Main scaffolding method"""
        log(f"🚀 Creating new project: {Colors.BOLD}{self.title_case_name}{Colors.RESET}", Colors.CYAN)
        log(f"📍 Target directory: {self.target_dir}", Colors.BLUE)
        
        # Check if target directory already exists
        if self.target_dir.exists():
            if any(self.target_dir.iterdir()):
                log(f"❌ Target directory is not empty: {self.target_dir}", Colors.RED)
                response = input(f"{Colors.YELLOW}Continue anyway? (y/N): {Colors.RESET}")
                if response.lower() != 'y':
                    log("❌ Scaffolding cancelled", Colors.RED)
                    return False
        else:
            # Create target directory
            self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # Execute scaffolding steps
        steps = [
            ("Copying template structure", self.copy_template_structure),
            ("Updating file contents", self.update_file_contents),
            ("Initializing git repository", self.initialize_git_repository),
            ("Setting up development environment", self.setup_development_environment),
        ]
        
        for step_name, step_func in steps:
            log(f"\n🔄 {step_name}...", Colors.MAGENTA)
            if not step_func():
                log(f"❌ Failed at step: {step_name}", Colors.RED)
                return False
        
        # Create project summary
        self.create_project_summary()
        
        log(f"\n🎉 {Colors.BOLD}Project created successfully!{Colors.RESET}", Colors.GREEN)
        self.print_next_steps()
        
        return True

    def print_next_steps(self) -> None:
        """Print next steps for the user"""
        log(f"\n📋 {Colors.BOLD}Next Steps:{Colors.RESET}", Colors.CYAN)
        log(f"\n1. Navigate to your project:", Colors.WHITE)
        log(f"   cd {self.target_dir}", Colors.BLUE)
        
        log(f"\n2. Start development servers:", Colors.WHITE)
        log(f"   # Terminal 1 (Backend)", Colors.BLUE)
        log(f"   cd backend", Colors.BLUE)
        log(f"   source venv/bin/activate  # Windows: venv\\Scripts\\activate", Colors.BLUE)
        log(f"   python dev.py server", Colors.BLUE)
        
        log(f"\n   # Terminal 2 (Frontend)", Colors.BLUE)
        log(f"   cd frontend", Colors.BLUE)
        log(f"   node dev.js server", Colors.BLUE)
        
        log(f"\n3. Access your application:", Colors.WHITE)
        log(f"   Frontend: http://localhost:5173", Colors.BLUE)
        log(f"   Backend:  http://localhost:8000", Colors.BLUE)
        log(f"   API Docs: http://localhost:8000/docs", Colors.BLUE)
        
        log(f"\n4. Read documentation:", Colors.WHITE)
        log(f"   README.md - Project overview", Colors.BLUE)
        log(f"   DEVELOPMENT.md - Development setup", Colors.BLUE)
        log(f"   DEPLOYMENT.md - Production deployment", Colors.BLUE)
        log(f"   WORKFLOW.md - Team workflows", Colors.BLUE)
        log(f"   PROJECT_SUMMARY.md - Quick reference", Colors.BLUE)
        
        log(f"\n🚀 {Colors.BOLD}Happy coding!{Colors.RESET}", Colors.GREEN)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Scaffold a new full-stack web application from starter template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scaffold.py
  python scaffold.py --name my-awesome-app
  python scaffold.py --name blog-platform --description "A modern blogging platform"
  python scaffold.py --name ecommerce --target ../my-projects/ecommerce

The scaffold tool will:
- Copy the template structure to a new directory
- Replace template names with your project name
- Initialize a git repository with initial commit
- Set up environment files
- Install dependencies (if tools are available)
- Create comprehensive documentation
        """
    )
    
    parser.add_argument(
        '--name', '-n',
        help='Project name (lowercase, hyphens allowed)',
        default=None
    )
    
    parser.add_argument(
        '--description', '-d',
        help='Project description',
        default='A full-stack web application built with FastAPI and React'
    )
    
    parser.add_argument(
        '--target', '-t',
        help='Target directory (default: ./PROJECT_NAME)',
        default=None
    )
    
    parser.add_argument(
        '--skip-deps',
        action='store_true',
        help='Skip dependency installation'
    )
    
    args = parser.parse_args()
    
    # Get project name
    if args.name:
        project_name = args.name
    else:
        project_name = input(f"{Colors.CYAN}Enter project name: {Colors.RESET}").strip()
    
    if not project_name:
        log("❌ Project name is required", Colors.RED)
        sys.exit(1)
    
    # Sanitize project name
    original_name = project_name
    project_name = sanitize_name(project_name)
    
    if project_name != original_name:
        log(f"📝 Project name sanitized: {original_name} → {project_name}", Colors.YELLOW)
    
    # Validate project name
    if not validate_project_name(project_name):
        log(f"❌ Invalid project name: {project_name}", Colors.RED)
        log("Project name must be lowercase, start with a letter, and contain only letters, numbers, hyphens, and underscores", Colors.YELLOW)
        sys.exit(1)
    
    # Get description
    description = args.description
    if not description or description == 'A full-stack web application built with FastAPI and React':
        user_description = input(f"{Colors.CYAN}Enter project description (optional): {Colors.RESET}").strip()
        if user_description:
            description = user_description
    
    # Determine target directory
    if args.target:
        target_dir = args.target
    else:
        target_dir = f"./{project_name}"
    
    # Create scaffolder and run
    scaffolder = ProjectScaffolder(project_name, description, target_dir)
    
    try:
        success = scaffolder.scaffold()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        log("\n❌ Scaffolding interrupted by user", Colors.RED)
        sys.exit(1)
    except Exception as e:
        log(f"\n❌ Unexpected error: {e}", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()