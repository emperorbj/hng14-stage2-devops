#!/bin/bash
echo "Running all containers"
docker compose down
docker builder prune -f
docker compose build --no-cache
docker compose up