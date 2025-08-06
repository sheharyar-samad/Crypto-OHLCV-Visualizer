# run_chart.py
from data_fetcher import get_binance_ohlcv
from indicators import add_indicators
from chart import plot_chart

df = get_binance_ohlcv()
df = add_indicators(df)
plot_chart(df)
