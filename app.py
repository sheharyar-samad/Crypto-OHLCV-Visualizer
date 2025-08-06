import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from data_fetcher import get_binance_ohlcv
from indicators import add_indicators

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Crypto Trading Chart"),

    # Coin selection dropdown
    dcc.Dropdown(
        id='symbol-dropdown',
        options=[
            {'label': 'BTC/USDT', 'value': 'BTCUSDT'},
            {'label': 'ETH/USDT', 'value': 'ETHUSDT'},
            {'label': 'BNB/USDT', 'value': 'BNBUSDT'},
            {'label': 'ADA/USDT', 'value': 'ADAUSDT'},
        ],
        value='BTCUSDT',
        clearable=False,
        style={'width': '200px', 'margin-bottom': '20px'}
    ),

    # Timeframe dropdown
    dcc.Dropdown(
        id='interval-dropdown',
        options=[
            {'label': '1 minute', 'value': '1m'},
            {'label': '3 minutes', 'value': '3m'},
            {'label': '5 minutes', 'value': '5m'},
            {'label': '15 minutes', 'value': '15m'},
        ],
        value='1m',
        clearable=False,
        style={'width': '200px', 'margin-bottom': '20px'}
    ),

    # Indicator selection dropdown
    dcc.Dropdown(
        id='indicator-dropdown',
        options=[
            {'label': 'RSI', 'value': 'rsi'},
            {'label': 'Support & Resistance (Pivot Points)', 'value': 'sr'},
            {'label': 'Moving Average (SMA 20)', 'value': 'sma'},
            {'label': 'Bollinger Bands', 'value': 'bb'},
        ],
        value='rsi',
        clearable=False,
        style={'width': '300px', 'margin-bottom': '20px'}
    ),

    # Auto-refresh interval (1 minute)
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,  # 1 minute in ms
        n_intervals=0
    ),

    dcc.Graph(id='candlestick-chart')
])


@app.callback(
    Output('candlestick-chart', 'figure'),
    [
        Input('symbol-dropdown', 'value'),
        Input('interval-dropdown', 'value'),
        Input('indicator-dropdown', 'value'),
        Input('interval-component', 'n_intervals'),
    ]
)
def update_chart(symbol, interval, indicator, n_intervals):
    df = get_binance_ohlcv(symbol=symbol, interval=interval, limit=100)
    df = add_indicators(df)

    fig = go.Figure()

    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Candles'
    ))

    # Add selected indicator
    if indicator == 'rsi':
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['rsi'],
            mode='lines',
            name='RSI',
            line=dict(color='purple', width=2)
        ))
        fig.update_layout(yaxis_title='Price', yaxis2=dict(title='RSI', overlaying='y', side='right', range=[0, 100]))

    elif indicator == 'sma':
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['sma_20'],
            mode='lines',
            name='SMA 20',
            line=dict(color='blue', width=2)
        ))

    elif indicator == 'bb':
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['bb_upper'],
            mode='lines',
            name='Bollinger Upper Band',
            line=dict(color='green', width=1, dash='dot')
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['bb_mid'],
            mode='lines',
            name='Bollinger Middle Band',
            line=dict(color='orange', width=1)
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['bb_lower'],
            mode='lines',
            name='Bollinger Lower Band',
            line=dict(color='green', width=1, dash='dot')
        ))

    elif indicator == 'sr':  # Support & Resistance (pivot points)
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['pivot'],
            mode='lines',
            name='Pivot',
            line=dict(color='gold', width=1, dash='dash')
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['support1'],
            mode='lines',
            name='Support 1',
            line=dict(color='red', width=1, dash='dot')
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['support2'],
            mode='lines',
            name='Support 2',
            line=dict(color='red', width=1, dash='dot')
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['resistance1'],
            mode='lines',
            name='Resistance 1',
            line=dict(color='green', width=1, dash='dot')
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['resistance2'],
            mode='lines',
            name='Resistance 2',
            line=dict(color='green', width=1, dash='dot')
        ))

    fig.update_layout(
        title=f'{symbol} Candlestick Chart with {indicator.upper()} Indicator',
        xaxis_title='Time',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
