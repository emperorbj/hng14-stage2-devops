#!/usr/bin/env bash
set -euo pipefail

timeout 120 docker compose up -d --build

timeout 90 bash -c 'until curl -sf http://localhost:8000/health; do
  echo "Waiting for API..."
  sleep 3
done'

timeout 90 bash -c 'until curl -sf http://localhost:3000/health; do
  echo "Waiting for frontend..."
  sleep 3
done'

echo "integration.sh smoke checks passed"

docker compose down -v
