source .dbcfg
docker run -it --rm --link moksha-postgres:postgres postgres psql -h postgres -U "$POSTGRES_USER"

