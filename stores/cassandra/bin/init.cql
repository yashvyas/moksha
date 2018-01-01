CREATE KEYSPACE IF NOT EXISTS binance WITH replication = {'class':'SimpleStrategy', 'replication_factor':1};
USE binance;
CREATE TABLE trades (
  event varchar,
  etime timestamp,
  symbol varchar,
  atradeid bigint,
  price float,
  quantity float,
  ttime timestamp,
  ftradeid bigint,
  ltradeid bigint,
  maker boolean,
  PRIMARY KEY (ttime)
);
