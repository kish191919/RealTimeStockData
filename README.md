# 📈 Real-Time Stock Data Pipeline with Kafka, Spark, PostgreSQL, and Grafana

## Overview

This project demonstrates a real-time data pipeline that ingests stock price data for Palantir (PLTR) and Amazon (AMZN) using Kafka, processes it with Spark, stores it in PostgreSQL, and visualizes it through Grafana. The pipeline also includes an LSTM-based model for predicting future stock prices.

## Architecture

```
[Yahoo Finance] → [Kafka] → [Spark Streaming] → [PostgreSQL] → [Grafana]
                                        ↓
                                 [LSTM Prediction]
```

## Features

* Real-time stock data ingestion using `yfinance`
* Kafka messaging for streaming transport
* Spark Structured Streaming for ETL processing
* PostgreSQL for structured data storage
* Grafana for time series visualization
* LSTM model for next-day stock price forecasting

## Setup Instructions

### 1. EC2 Server Preparation

* Ubuntu 22.04 EC2 instance (t2.medium+ recommended)
* Open ports: 22, 9092, 4040, 3000
* SSH into instance:

```bash
ssh -i "YOUR_KEY.pem" ubuntu@<EC2_PUBLIC_IP>
```

### 2. Environment Setup

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip openjdk-11-jdk git unzip wget -y
mkdir stock && cd stock
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
```

### 3. Kafka Setup

```bash
wget https://downloads.apache.org/kafka/3.7.2/kafka_2.12-3.7.2.tgz
 tar -xzf kafka_2.12-3.7.2.tgz && mv kafka_2.12-3.7.2 kafka && cd kafka
nohup bin/zookeeper-server-start.sh config/zookeeper.properties &
nohup bin/kafka-server-start.sh config/server.properties &
bin/kafka-topics.sh --create --topic stocks --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 4. Python Stock Producer

```bash
pip install yfinance kafka-python
python3 stock_producer.py  # provided in source code
```

### 5. Spark Setup

```bash
wget https://downloads.apache.org/spark/spark-3.4.4/spark-3.4.4-bin-hadoop3.tgz
 tar -xzf spark-3.4.4-bin-hadoop3.tgz && mv spark-3.4.4-bin-hadoop3 spark && cd spark
pip install pyspark
```

### 6. PostgreSQL Setup

```bash
sudo apt install postgresql postgresql-contrib -y
sudo -u postgres psql
```

Inside PostgreSQL:

```sql
CREATE DATABASE stockdb;
CREATE USER stock WITH PASSWORD 'stock123';
GRANT ALL PRIVILEGES ON DATABASE stockdb TO stock;
\c stockdb
GRANT USAGE ON SCHEMA public TO stock;
GRANT CREATE ON SCHEMA public TO stock;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO stock;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO stock;
```

### 7. Create Table

```sql
CREATE TABLE stock_price (
  symbol TEXT,
  timestamp TEXT,
  open FLOAT,
  high FLOAT,
  low FLOAT,
  close FLOAT,
  volume FLOAT
);
```

### 8. Spark to PostgreSQL

```bash
wget https://jdbc.postgresql.org/download/postgresql-42.7.3.jar -P ~/spark/jars/
~/spark/bin/spark-submit --jars ~/spark/jars/postgresql-42.7.3.jar --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.4 stock_spark_process_stream.py
```

### 9. Grafana Setup

```bash
sudo apt install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo apt update && sudo apt install grafana -y
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

### 10. Grafana Dashboard

* Connect PostgreSQL as data source
* Create dashboard panels with SQL like:

```sql
SELECT
  timestamp AS "time",
  close AS "Close Price"
FROM stock_price
WHERE symbol = 'PLTR'
ORDER BY timestamp ASC;
```

### 11. LSTM Prediction

* Predict next-day stock prices using `predict_lstm.py`
* Requires: `pandas`, `numpy`, `tensorflow`, `scikit-learn`, `psycopg2`

### 12. Automate with Cron

```bash
crontab -e
0 8 * * * /home/ubuntu/stock/venv/bin/python3 /home/ubuntu/stock/predict_lstm.py >> /home/ubuntu/stock/predict.log 2>&1
```

---

## License

MIT License

