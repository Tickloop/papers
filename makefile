@PHONY: repave-db
repave-db:
	@echo "Repaving the database..."
	- docker compose down
	- docker container rm lava-pg
	- docker volume rm lava-pg
	- docker volume create lava-pg
	- docker compose up -d
	- cd server && sleep 5 && alembic upgrade head
	@echo "Database repaved successfully."