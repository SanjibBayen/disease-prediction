.PHONY: help setup backend run-backend clean test docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make setup         - Setup backend environment"
	@echo "  make run-backend   - Run backend server"
	@echo "  make test          - Run API tests"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"
	@echo "  make clean         - Clean Python cache files"

setup:
	@echo "Setting up backend..."
	cd backend && python -m venv venv
	cd backend && source venv/bin/activate || cd backend && venv\\Scripts\\activate
	cd backend && pip install -r requirements.txt
	@echo "Setup complete!"

run-backend:
	@echo "Starting backend server..."
	cd backend && python run.py

test:
	@echo "Running API tests..."
	powershell -ExecutionPolicy Bypass -File test_api.ps1

docker-build:
	@echo "Building Docker image..."
	docker-compose build

docker-run:
	@echo "Running Docker container..."
	docker-compose up -d
	@echo "Backend running at http://localhost:8000"

docker-stop:
	@echo "Stopping Docker container..."
	docker-compose down

docker-logs:
	@echo "Showing logs..."
	docker-compose logs -f

clean:
	@echo "Cleaning Python cache..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Clean complete!"

clean-all: clean
	@echo "Removing virtual environment..."
	rm -rf backend/venv
	rm -rf backend/logs
	rm -rf backend/temp
	@echo "Complete clean done!"