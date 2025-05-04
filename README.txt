🐍 Django Dockerized Project

Minimal Django setup using Docker & Docker Compose. Supports both local development with runserver and lightweight production using gunicorn.

📦 Requirements

Docker

Docker Compose

(optional) Python 3.11+ & pip — only if using venv locally

📁 Project Structure

.
├── app/                      # Django project
├── Dockerfile                # Dev: uses runserver
├── Dockerfile.prod           # Prod: uses gunicorn
├── docker-compose.yml        # Local development setup
├── docker-compose.prod.yml   # Production (no SSL)
├── entrypoint.sh             # DB wait + migrate
├── requirements.txt
├── .env                      # Environment config
└── README.md

⚙️ .env example

Create a .env file in the root directory:

# Debug mode
DEBUG=1

# Allowed hosts
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# MySQL credentials
MYSQL_DATABASE=djangodatabase
MYSQL_USER=superadmin
MYSQL_PASSWORD=superadmin
MYSQL_ROOT_PASSWORD=superadmin

# Django DB connection
DATABASE_NAME=djangodatabase
DATABASE_USER=superadmin
DATABASE_PASSWORD=superadmin
DATABASE_HOST=db
DATABASE_PORT=3306

🧪 Local Development

Run Django dev server via runserver:

docker compose up --build

Useful commands:

docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose logs -f

Stop:

docker compose down

🚀 Production Mode (Gunicorn)

Runs Django with gunicorn, no SSL:

docker compose -f docker-compose.prod.yml up --build

Run in background:

docker compose -f docker-compose.prod.yml up -d

Stop:

docker compose -f docker-compose.prod.yml down

Rebuild from scratch:

docker compose -f docker-compose.prod.yml build --no-cache

🔑 Entrypoint Logic

entrypoint.sh does the following:

Waits for the DB to be ready

Applies all Django migrations

Executes the given command (e.g. gunicorn or runserver)

🧠 Notes

Admin user is not auto-created: run createsuperuser manually.

Static files are not yet served in production — add Nginx or use WhiteNoise if needed.

entrypoint.sh must be executable: chmod +x entrypoint.sh

🛉 Optional Cleanup

docker system prune -af  # removes unused images/containers
docker builder prune -af # clears Docker build cache


