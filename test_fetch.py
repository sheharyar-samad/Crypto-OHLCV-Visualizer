from data_fetcher import get_binance_ohlcv

df = get_binance_ohlcv()
print(df.head())
