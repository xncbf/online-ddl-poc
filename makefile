migrate:
	@echo "마이그레이션을 시작합니다..."
	@docker build -t my-flyway .
	@docker run --rm --env-file .env my-flyway -configFiles=/flyway/conf/flyway.conf -X migrate
	@echo "마이그레이션이 완료되었습니다."

baseline:
	@echo "Baseline을 시작합니다..."
	@docker run --rm --env-file .env my-flyway -configFiles=/flyway/conf/flyway.conf -X baseline
	@echo "Baseline이 완료되었습니다."

run:
	@echo "Stopping any running Uvicorn and Locust processes..."
	@pkill -f "uvicorn app.main:app" || true
	@pkill -f "locust" || true
	lsof -ti :8080 | xargs kill -9
	@sleep 1
	@echo "Starting Uvicorn and Locust..."
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 10 & \
	locust -H http://localhost:8080 & \
	wait
