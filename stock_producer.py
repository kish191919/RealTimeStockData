
# stock_producer.py
import yfinance as yf
import json, time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

tickers = ['PLTR', 'AMZN']

while True:
    for symbol in tickers:
        data = yf.Ticker(symbol).history(period='1d', interval='1m').tail(1)
        for _, row in data.iterrows():
            record = {
                'symbol': symbol,
                'timestamp': row.name.strftime('%Y-%m-%d %H:%M:%S'),
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': row['Volume']
            }
            producer.send('stocks', value=record)
            print(f"Sent: {record}")
    time.sleep(60)


