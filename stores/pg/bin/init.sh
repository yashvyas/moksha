#!/usr/bin/env bash
set -x
source .dbcfg
docker exec -it -e PGPASSWORD="$POSTGRES_PASSWORD" moksha-postgres psql -U "$POSTGRES_USER" -f /tmp/init.sql

