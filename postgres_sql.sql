sudo -u postgres psql

-- 1. Create the database and user
CREATE DATABASE stockdb;
CREATE USER stock WITH PASSWORD 'stock123';

-- 2. Grant the stock user access to the stockdb database
GRANT ALL PRIVILEGES ON DATABASE stockdb TO stock;

-- 3. Connect to the stockdb database
\c stockdb

-- 4. Grant usage and create permissions on the public schema (important!)
GRANT USAGE ON SCHEMA public TO stock;
GRANT CREATE ON SCHEMA public TO stock;

-- 5. Grant privileges on existing tables in the public schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO stock;

-- 6. Automatically grant privileges on tables created in the future
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO stock;



-- change to stockdb 
\c stockdb

-- stockdb to create the table
CREATE TABLE stock_price (
  symbol TEXT,
  timestamp TEXT,
  open FLOAT,
  high FLOAT,
  low FLOAT,
  close FLOAT,
  volume FLOAT
);

