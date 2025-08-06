# test_indicators.py
from data_fetcher import get_binance_ohlcv
from indicators import add_indicators

df = get_binance_ohlcv()
df = add_indicators(df)
print(df.tail())
