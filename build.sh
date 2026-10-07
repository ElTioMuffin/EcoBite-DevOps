#!/bin/bash
set -e

# Wait for DB
host="${DATABASE_HOST:-DATABASE_URL}"
port="${DATABASE_PORT:-5432}"
until nc -z "$host" "$port"; do
  echo "Waiting for Postgres at $host:$port..."
  sleep 1
done

# Apply migrations & collectstatic (optional - you can remove collectstatic in prod if using build-time)
python manage.py migrate --noinput
python manage.py generate_test_data --noinput
python manage.py collectstatic --noinput

# Create a superuser automatically if needed (optional)
# python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

exec "$@"
