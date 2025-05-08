
# stock_data.py
import yfinance as yf
import json, time

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
            print(record)
    time.sleep(60)  # 1분마다


