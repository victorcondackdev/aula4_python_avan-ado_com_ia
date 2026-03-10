#!/bin/sh
set -e

RETRIES="${DB_CONNECT_RETRIES:-30}"
SLEEP_SECONDS="${DB_CONNECT_SLEEP_SECONDS:-2}"
ATTEMPT=1
DB_HOST="${DB_HOST:-db}"

while [ "$ATTEMPT" -le "$RETRIES" ]; do
  if getent hosts "$DB_HOST" >/dev/null 2>&1; then
    break
  fi

  echo "DNS ainda nao resolveu host '${DB_HOST}' (tentativa ${ATTEMPT}/${RETRIES}). Aguardando ${SLEEP_SECONDS}s..."
  ATTEMPT=$((ATTEMPT + 1))
  sleep "$SLEEP_SECONDS"
done

if [ "$ATTEMPT" -gt "$RETRIES" ]; then
  echo "Falha ao resolver host '${DB_HOST}' apos ${RETRIES} tentativas."
  exit 1
fi

ATTEMPT=1

while [ "$ATTEMPT" -le "$RETRIES" ]; do
  if python manage.py migrate --noinput; then
    break
  fi

  echo "Migrate falhou (tentativa ${ATTEMPT}/${RETRIES}). Aguardando ${SLEEP_SECONDS}s..."
  ATTEMPT=$((ATTEMPT + 1))
  sleep "$SLEEP_SECONDS"
done

if [ "$ATTEMPT" -gt "$RETRIES" ]; then
  echo "Nao foi possivel aplicar migracoes apos ${RETRIES} tentativas."
  exit 1
fi

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 60
