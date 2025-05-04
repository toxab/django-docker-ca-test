# Check if docker-compose.override.yml exists
override_file := $(shell [ -f docker-compose.override.yml ] && echo "-f docker-compose.override.yml" || echo "")

# Local development
up:
	docker-compose -f docker-compose.yml $(override_file) up --build

down:
	docker-compose -f docker-compose.yml $(override_file) down

migrate:
	docker-compose -f docker-compose.yml $(override_file) exec web python manage.py migrate

createsuperuser:
	docker-compose -f docker-compose.yml $(override_file) exec web python manage.py createsuperuser

logs:
	docker-compose -f docker-compose.yml $(override_file) logs -f

build:
	docker-compose -f docker-compose.yml $(override_file) build

# Production
prod-up:
	docker-compose -f docker-compose.prod.yml up --build

prod-up-detached:
	docker-compose -f docker-compose.prod.yml up -d --build

prod-down:
	docker-compose -f docker-compose.prod.yml down

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f

prod-build:
	docker-compose -f docker-compose.prod.yml build

prod-migrate:
	docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

prod-createsuperuser:
	docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Cleaning
prune:
	docker system prune -af
