#!/bin/sh
set -eu

if [ -n "${DATABASE_URL:-}" ]; then
  DB_HOST="$(python -c 'import os,dj_database_url; print(dj_database_url.parse(os.environ["DATABASE_URL"]).get("HOST") or "localhost")')"
  DB_PORT="$(python -c 'import os,dj_database_url; print(dj_database_url.parse(os.environ["DATABASE_URL"]).get("PORT") or "5432")')"
  DB_NAME="$(python -c 'import os,dj_database_url; print(dj_database_url.parse(os.environ["DATABASE_URL"]).get("NAME") or "")')"
  DB_USER="$(python -c 'import os,dj_database_url; print(dj_database_url.parse(os.environ["DATABASE_URL"]).get("USER") or "")')"

  echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
  until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" >/dev/null 2>&1; do
    sleep 2
  done
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
