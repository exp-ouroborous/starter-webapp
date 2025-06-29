# Frontend Development Makefile
# Provides common development tasks

.PHONY: help setup server build preview test lint fix clean deploy

# Default target
help:
	@echo "🛠️  Frontend Development Commands"
	@echo ""
	@echo "Setup & Development:"
	@echo "  make setup      - Set up development environment"
	@echo "  make server     - Start development server"
	@echo "  make build      - Build for production"
	@echo "  make preview    - Preview production build"
	@echo "  make test       - Run tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint       - Run linting checks"
	@echo "  make fix        - Fix formatting and linting issues"
	@echo "  make clean      - Clean up build files"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy     - Deploy to production"
	@echo "  make deploy-dev - Deploy to development"
	@echo "  make deploy-preview - Deploy to preview"
	@echo ""
	@echo "Analysis:"
	@echo "  make analyze    - Analyze bundle size"
	@echo ""
	@echo "Examples:"
	@echo "  make setup"
	@echo "  make server"
	@echo "  make build"

# Setup development environment
setup:
	@node dev.js setup

# Start development server
server:
	@node dev.js server

# Build for production
build:
	@node dev.js build

# Preview production build
preview:
	@node dev.js preview

# Run tests
test:
	@node dev.js test

# Code quality
lint:
	@node dev.js lint

fix:
	@node dev.js fix

# Cleanup
clean:
	@node dev.js clean

# Analysis
analyze:
	@node dev.js analyze

# Deployment
deploy:
	@node dev.js deploy production

deploy-dev:
	@node dev.js deploy development

deploy-preview:
	@node dev.js deploy preview

# Install dependencies (for CI/CD)
install:
	@npm install

# Type checking
type-check:
	@npm run type-check