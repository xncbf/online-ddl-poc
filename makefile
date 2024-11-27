.PHONY: run

run:
	@echo "Stopping any running Uvicorn and Locust processes..."
	@pkill -f "uvicorn app.main:app" || true
	@pkill -f "locust" || true
	lsof -ti :8080 | xargs kill -9
	@sleep 1
	@echo "Starting Uvicorn and Locust..."
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 4 & \
	locust -H http://localhost:8080 & \
	wait
