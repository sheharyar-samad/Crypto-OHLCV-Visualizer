import pandas as pd
import ta

def add_indicators(df):
    # Ensure numeric and fill NaNs in 'close'
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['close'].fillna(method='ffill', inplace=True)

    rsi = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
    df['rsi'] = rsi.fillna(method='ffill')

    # Simple Moving Average (20 period)
    if len(df) >= 20:
        sma_indicator = ta.trend.SMAIndicator(close=df['close'], window=20)
        df['sma_20'] = sma_indicator.sma_indicator()
    else:
        df['sma_20'] = None

    # Bollinger Bands (20 period, 2 std)
    if len(df) >= 20:
        bb_indicator = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
        df['bb_upper'] = bb_indicator.bollinger_hband()
        df['bb_lower'] = bb_indicator.bollinger_lband()
        df['bb_mid'] = bb_indicator.bollinger_mavg()
    else:
        df['bb_upper'] = None
        df['bb_lower'] = None
        df['bb_mid'] = None

    # Pivot Points (Classic) Support & Resistance Levels
    # Calculate pivot points using OHLC
    if len(df) >= 2:
        df['pivot'] = (df['high'].shift(1) + df['low'].shift(1) + df['close'].shift(1)) / 3
        df['support1'] = (2 * df['pivot']) - df['high'].shift(1)
        df['support2'] = df['pivot'] - (df['high'].shift(1) - df['low'].shift(1))
        df['resistance1'] = (2 * df['pivot']) - df['low'].shift(1)
        df['resistance2'] = df['pivot'] + (df['high'].shift(1) - df['low'].shift(1))
    else:
        df['pivot'] = None
        df['support1'] = None
        df['support2'] = None
        df['resistance1'] = None
        df['resistance2'] = None

    return df
