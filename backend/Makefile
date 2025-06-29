# Backend Development Makefile
# Provides common development tasks

.PHONY: help setup server test clean lint format db-reset db-migrate db-upgrade

# Default target
help:
	@echo "🛠️  Backend Development Commands"
	@echo ""
	@echo "Setup & Development:"
	@echo "  make setup      - Set up development environment"
	@echo "  make server     - Start development server"
	@echo "  make test       - Run tests"
	@echo ""
	@echo "Database:"
	@echo "  make db-upgrade - Apply database migrations"
	@echo "  make db-migrate - Create new migration (MESSAGE=description)"
	@echo "  make db-reset   - Reset database (WARNING: deletes data)"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code automatically"
	@echo "  make clean      - Clean up development files"
	@echo ""
	@echo "Examples:"
	@echo "  make setup"
	@echo "  make server"
	@echo "  make db-migrate MESSAGE='add user table'"

# Setup development environment
setup:
	@python dev.py setup

# Start development server
server:
	@python dev.py server

# Run tests
test:
	@python dev.py test

# Database operations
db-upgrade:
	@python dev.py db-upgrade

db-migrate:
	@python dev.py db-migrate "$(MESSAGE)"

db-reset:
	@python dev.py db-reset

# Code quality
lint:
	@python dev.py lint

format:
	@python dev.py format

# Cleanup
clean:
	@python dev.py clean

# Install dependencies (for CI/CD)
install:
	@pip install -r requirements.txt

# Production build
build:
	@echo "🏗️  Building for production..."
	@pip install -r requirements.txt
	@alembic upgrade head
	@echo "✅ Build complete"