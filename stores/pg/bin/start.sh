#!/usr/bin/env bash
mkdir -p .data
chmod a+rwx .data
source .dbcfg
docker run -d --name moksha-postgres -e POSTGRES_PASSWORD -e POSTGRES_USER -v $(pwd)/.data:/var/lib/postgresql/data -v $(pwd)/init.sql:/tmp/init.sql postgres
