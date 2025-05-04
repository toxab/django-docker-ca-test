#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status

echo "🕒 Waiting for the database at $DATABASE_HOST:$DATABASE_PORT..."

# Wait until the database is ready to accept connections
while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  sleep 1
done

echo "✅ Database is up!"

# Apply Django database migrations
echo "📦 Applying database migrations..."
python manage.py migrate --noinput

if [ "$(python manage.py shell -c 'from inventory.models import Ingredient; print(Ingredient.objects.exists())')" = "False" ]; then
    echo "📥 Loading fixture data..."
    python manage.py loaddata inventory/fixtures/initial_data.json
else
    echo "✔ Fixture data already loaded."

# Optional: collect static files (useful for production)
# echo "📁 Collecting static files..."
# python manage.py collectstatic --noinput

# Execute the main command passed to the container (e.g., gunicorn, runserver)
echo "🚀 Starting the application..."
exec "$@"
