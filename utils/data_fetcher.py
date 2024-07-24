import requests
import pandas as pd
import plotly.graph_objects as go

API_KEY = 'OX8PKTP2LZZZ7JO8'

def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

def process_stock_data(data):
    df = pd.DataFrame(data['Time Series (5min)']).T
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    return df

def get_processed_stock_data(symbol):
    data = get_stock_data(symbol)
    return process_stock_data(data)

def create_stock_chart(df):
    fig = go.Figure(data=[go.Scatter(x=df.index, y=df['close'], mode='lines', name='Close')])
    fig.update_layout(title='Preço de Fechamento', xaxis_title='Tempo', yaxis_title='Preço')
    return fig
