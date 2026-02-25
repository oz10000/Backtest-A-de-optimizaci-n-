import requests
import pandas as pd
import time

LIMIT = 1000

def fetch_klines(symbol='BTCUSDT', interval='1m', hours=168):  # 1 semana
    base_url = 'https://api.binance.com/api/v3/klines'
    end_time = int(time.time() * 1000)
    start_time = end_time - hours * 60 * 60 * 1000
    all_klines = []
    current_start = start_time

    while current_start < end_time:
        params = {'symbol': symbol, 'interval': interval, 'startTime': current_start, 'limit': LIMIT}
        try:
            resp = requests.get(base_url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if not data: break
            all_klines.extend(data)
            current_start = data[-1][0] + 1
        except Exception as e:
            print(f"Error en descarga: {e}")
            break

    columns = ['timestamp','open','high','low','close','volume','close_time','quote_asset_volume','number_of_trades','taker_buy_base_asset_volume','taker_buy_quote_asset_volume','ignore']
    df = pd.DataFrame(all_klines, columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    for col in ['open','high','low','close','volume']:
        df[col] = df[col].astype(float)
    return df[['open','high','low','close','volume']]
