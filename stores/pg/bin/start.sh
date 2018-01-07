#!/usr/bin/env bash
mkdir -p .data
chmod a+rwx .data
source .dbcfg
docker run -d --name moksha-postgres -e PGPASSWORD="$POSTGRES_PASSWORD" -e POSTGRES_PASSWORD -e POSTGRES_USER -p 5432:5432 -v $(pwd)/.data:/var/lib/postgresql/data -v $(pwd)/init.sql:/tmp/init.sql postgres
