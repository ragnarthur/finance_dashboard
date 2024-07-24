import os
import requests
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

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

def create_stock_chart(df, symbol):
    fig = go.Figure(data=[go.Scatter(x=df.index, y=df['close'], mode='lines', name=symbol)])
    fig.update_layout(title=f'Preço de Fechamento: {symbol}', xaxis_title='Tempo', yaxis_title='Preço')
    return fig

def get_top_5_stocks():
    # Lista de símbolos das ações para monitorar
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    top_stocks = []

    for symbol in symbols:
        data = get_stock_data(symbol)
        df = process_stock_data(data)
        last_close = df['close'].iloc[-1]
        top_stocks.append((symbol, last_close))

    # Ordenar as ações pelo preço de fechamento mais recente em ordem decrescente
    top_stocks.sort(key=lambda x: x[1], reverse=True)

    return top_stocks[:5]
