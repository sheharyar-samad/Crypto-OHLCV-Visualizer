import plotly.graph_objects as go

def create_chart(df, indicator):
    fig = go.Figure()

    # Add candlestick
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Candlestick'
    ))

    if indicator == 'support_resistance':
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['pivot'],
            mode='lines', name='Pivot Point',
            line=dict(color='blue', width=2, dash='dash')
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['support_1'],
            mode='lines', name='Support 1',
            line=dict(color='green', width=1.5, dash='dot')
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['support_2'],
            mode='lines', name='Support 2',
            line=dict(color='green', width=1, dash='dot')
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['resistance_1'],
            mode='lines', name='Resistance 1',
            line=dict(color='red', width=1.5, dash='dot')
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['resistance_2'],
            mode='lines', name='Resistance 2',
            line=dict(color='red', width=1, dash='dot')
        ))

        fig.update_layout(
            yaxis=dict(title='Price'),
            xaxis_rangeslider_visible=False
        )

    elif indicator == 'rsi':
        # Plot RSI on secondary y-axis
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['rsi'],
            mode='lines', name='RSI',
            line=dict(color='purple', width=2)
        ))

        fig.update_layout(
            yaxis=dict(title='Price'),
            yaxis2=dict(
                title='RSI',
                overlaying='y',
                side='right',
                range=[0, 100],
                showgrid=False,
                position=1
            ),
            xaxis_rangeslider_visible=False,
            legend=dict(orientation='h', y=1.02, x=1)
        )
        # Link RSI trace to secondary y-axis
        fig.data[-1].update(yaxis='y2')

    elif indicator == 'ma':
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['ma'],
            mode='lines', name='Moving Average (20)',
            line=dict(color='orange', width=2)
        ))

        fig.update_layout(
            yaxis=dict(title='Price'),
            xaxis_rangeslider_visible=False
        )

    elif indicator == 'bollinger':
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['bb_upper'],
            mode='lines', name='BB Upper',
            line=dict(color='gray', width=1, dash='dot')
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['bb_lower'],
            mode='lines', name='BB Lower',
            line=dict(color='gray', width=1, dash='dot')
        ))

        fig.update_layout(
            yaxis=dict(title='Price'),
            xaxis_rangeslider_visible=False
        )

    else:
        fig.update_layout(
            yaxis=dict(title='Price'),
            xaxis_rangeslider_visible=False
        )

    fig.update_layout(
        title='Crypto Trading Chart',
        xaxis_title='Time',
        legend=dict(orientation='h', y=1.02, x=1)
    )

    return fig
