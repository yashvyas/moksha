CREATE DATABASE trades;
\connect trades;
CREATE TABLE IF NOT EXISTS binance (ttime bigint, price float8, qty float8, id int8);
