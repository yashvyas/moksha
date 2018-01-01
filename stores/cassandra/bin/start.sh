mkdir -p .data
docker run -d --name moksha-cassandra -v $(pwd)/.data:/var/lib/cassandra -v $(pwd)/init.cql:/tmp/init.cql cassandra
