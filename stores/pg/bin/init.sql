CREATE DATABASE trades;
\connect trades;
CREATE TABLE IF NOT EXISTS binance (key bigint, data json);
