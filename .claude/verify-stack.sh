#!/usr/bin/env bash
# Helper: run this from a terminal where `docker ps` works (fresh shell with
# the docker group). It builds, boots the stack, and probes each layer so
# Claude can drive end-to-end verification even though its own shells lack
# docker group access.
set -euo pipefail
cd "$(dirname "$0")"

echo "=== 0. compose config sanity ==="
docker compose config --quiet && echo "compose config OK"

echo "=== 1. build ==="
docker compose build api 2>&1 | tail -5

echo "=== 2. up (db, redis first) ==="
docker compose up -d db redis 2>&1 | tail -5
echo "waiting for healthy db+redis..."
for i in $(seq 1 30); do
  dbh=$(docker inspect -f '{{.State.Health.Status}}' "$(docker compose ps -q db)" 2>/dev/null || echo none)
  rdh=$(docker inspect -f '{{.State.Health.Status}}' "$(docker compose ps -q redis)" 2>/dev/null || echo none)
  echo "  db=$dbh redis=$rdh"
  [ "$dbh" = "healthy" ] && [ "$rdh" = "healthy" ] && break
  sleep 2
done

echo "=== 3. run migrations directly (proves alembic targets Postgres) ==="
docker compose run --rm api /bin/sh -c 'alembic upgrade head 2>&1 | tail -15'

echo "=== 4. verify migration actually wrote Postgres tables ==="
docker compose exec db psql -U postgres -d dbn_resume -c '\dt' 2>&1

echo "=== 5. boot full stack ==="
docker compose up -d 2>&1 | tail -15
sleep 8
echo "=== 6. container states ==="
docker compose ps
echo "=== 7. api /health ==="
docker compose exec api python -c "import urllib.request;print(urllib.request.urlopen('http://localhost:8000/health',timeout=5).read().decode())" 2>&1 || true
curl -sf http://localhost:8000/health 2>&1 || true

echo "=== 8. template download ==="
curl -sf -o /dev/null -w '%{http_code} %{content_type}\n' http://localhost:8000/api/v1/dbn-standards/template/download 2>&1 || true

echo "=== 9. active standard (proves seeded via init_db) ==="
curl -sf http://localhost:8000/api/v1/dbn-standards 2>&1 | head -c 400 || echo "(no curl / not up)"

echo "DONE"