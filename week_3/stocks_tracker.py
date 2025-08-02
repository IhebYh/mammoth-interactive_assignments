import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import yfinance as yf
import plotly.graph_objects as go

Tickers = {}
with open('stock_values.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                key, value = line.split(':')
                key = key.strip().strip("'").strip('"')
                value = value.strip().strip("'").strip('"')
                Tickers[key] = value
            except ValueError:
                continue

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Stock Price Dashboard", style={'textAlign': 'center'}),

    html.Label("Select Stocks:"),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': k, 'value': v} for k,v in Tickers.items()],
        value=[],
        multi=True
    ),

    html.Label("Select Period:"),
    dcc.Dropdown(
        id='period-dropdown',
        options=[
            {'label': '1 Month', 'value': '1mo'},
            {'label': '3 Months', 'value': '3mo'},
            {'label': '6 Months', 'value': '6mo'},
            {'label': '1 Year', 'value': '1y'},
            {'label': '2 Years', 'value': '2y'}
        ],
        value='3mo',
        clearable=False
    ),

    dcc.Graph(id='stock-chart', style={'height': '600px'})
])

@app.callback(
    Output('stock-chart', 'figure'),
    Input('ticker-dropdown', 'value'),
    Input('period-dropdown', 'value')
)
def update_stock_chart(selected_tickers, selected_period):
    if not selected_tickers:
        fig = go.Figure()
        fig.add_annotation(
            text="Select one or more stocks to view the chart",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=16)
        )
        fig.update_layout(template="plotly_white")
        return fig

    data = yf.download(selected_tickers, period=selected_period)['Close']

    fig = go.Figure()
    if isinstance(data, pd.Series):
        fig.add_trace(go.Scatter(x=data.index, y=data.values, mode='lines', name=selected_tickers))
    else:
        for ticker in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data[ticker], mode='lines', name=ticker))

    fig.update_layout(
        title=f"Stock Closing Prices ({selected_period})",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode="x unified",
        template="plotly_white"
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
