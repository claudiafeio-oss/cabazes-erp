#!/usr/bin/env bash
set -e
mkdir -p backups
docker compose exec -T db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "backups/backup_$(date +%Y%m%d_%H%M%S).sql"
