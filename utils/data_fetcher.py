import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Cache para armazenar os dados
cache = {}
cache_expiry = timedelta(minutes=5)  # Cache expira em 5 minutos

# Mapeamento de símbolos para nomes completos
company_names = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'GOOGL': 'Alphabet Inc.',
    'AMZN': 'Amazon.com Inc.',
    'TSLA': 'Tesla Inc.',
    'FB': 'Meta Platforms, Inc.',
    'NFLX': 'Netflix, Inc.',
    'NVDA': 'NVIDIA Corporation',
    'PYPL': 'PayPal Holdings, Inc.',
    'ADBE': 'Adobe Inc.'
}

def get_stock_data(symbol):
    # Verificar se os dados estão no cache
    if symbol in cache and (datetime.now() - cache[symbol]['timestamp']) < cache_expiry:
        return cache[symbol]['data']

    stock = yf.Ticker(symbol)
    data = stock.history(period="1d", interval="5m")

    # Verificar se os dados foram retornados corretamente
    if data.empty:
        raise ValueError(f"Erro ao obter dados para {company_names[symbol]}")

    # Armazenar os dados no cache
    cache[symbol] = {'data': data, 'timestamp': datetime.now()}
    return data

def process_stock_data(data):
    df = data.reset_index()
    df = df.rename(columns={'Datetime': 'timestamp', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'})
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    return df

def get_processed_stock_data(symbol):
    data = get_stock_data(symbol)
    return process_stock_data(data)

def create_stock_chart(df, symbol):
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()

    fig = go.Figure()
    
    # Adicionar linha de preço de fechamento
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name='Preço de Fechamento'))

    # Adicionar médias móveis
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['SMA_20'], mode='lines', name='Média Móvel 20'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['SMA_50'], mode='lines', name='Média Móvel 50'))

    # Atualizar layout para incluir eixo secundário
    fig.update_layout(
        title=f'Preço de Fechamento e Médias Móveis: {company_names[symbol]}',
        xaxis_title='Tempo',
        yaxis_title='Preço',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig

def create_volume_chart(df, symbol):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['timestamp'], y=df['volume'], name='Volume'))

    fig.update_layout(
        title=f'Volume de Negociação: {company_names[symbol]}',
        xaxis_title='Tempo',
        yaxis_title='Volume',
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig

def create_open_close_chart(df, symbol):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['open'], mode='lines', name='Preço de Abertura'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name='Preço de Fechamento'))

    fig.update_layout(
        title=f'Preço de Abertura e Fechamento: {company_names[symbol]}',
        xaxis_title='Tempo',
        yaxis_title='Preço',
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig

def get_top_5_stocks():
    # Lista de símbolos das ações para monitorar
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    top_stocks = []

    for symbol in symbols:
        try:
            data = get_stock_data(symbol)
            df = process_stock_data(data)
            last_close = df['close'].iloc[-1]
            open_price = df['open'].iloc[-1]
            volume = df['volume'].iloc[-1]
            percent_change = ((last_close - open_price) / open_price) * 100
            top_stocks.append((symbol, company_names[symbol], round(last_close, 2), volume, round(percent_change, 2)))
        except ValueError as e:
            print(e)
            continue

    # Ordenar as ações pelo preço de fechamento mais recente em ordem decrescente
    top_stocks.sort(key=lambda x: x[2], reverse=True)

    return top_stocks[:5]

def get_all_symbols():
    # Lista completa de símbolos a serem monitorados
    return company_names.keys()
