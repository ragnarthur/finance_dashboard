import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Cache para armazenar os dados com tempo de expiração de 5 minutos
cache = {}
cache_expiry = timedelta(minutes=5)

# Mapeamento de símbolos para nomes completos das empresas
company_names = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'GOOGL': 'Alphabet Inc.',
    'AMZN': 'Amazon.com Inc.',
    'TSLA': 'Tesla Inc.',
    'NFLX': 'Netflix, Inc.',
    'NVDA': 'NVIDIA Corporation',
    'PYPL': 'PayPal Holdings, Inc.',
    'ADBE': 'Adobe Inc.'
}

def get_stock_data(symbol):
    """
    Obtém dados históricos de ações para um determinado símbolo.
    
    Verifica se os dados estão no cache e se ainda não expiraram, caso contrário, busca novos dados da API.

    Args:
        symbol (str): O símbolo da ação para obter dados.

    Returns:
        pandas.DataFrame: Dados históricos da ação.
    """
    # Verificar se os dados estão no cache e se ainda estão válidos
    if symbol in cache and (datetime.now() - cache[symbol]['timestamp']) < cache_expiry:
        return cache[symbol]['data']

    # Buscar dados da ação usando yfinance
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d", interval="5m")

    # Verificar se os dados foram retornados corretamente
    if data.empty:
        raise ValueError(f"Erro ao obter dados para {company_names[symbol]}")

    # Armazenar os dados no cache
    cache[symbol] = {'data': data, 'timestamp': datetime.now()}
    return data

def process_stock_data(data):
    """
    Processa os dados da ação para renomear e selecionar colunas relevantes.

    Args:
        data (pandas.DataFrame): Dados da ação.

    Returns:
        pandas.DataFrame: Dados processados com colunas renomeadas.
    """
    df = data.reset_index()
    df = df.rename(columns={'Datetime': 'timestamp', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'})
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    return df

def get_processed_stock_data(symbol):
    """
    Obtém e processa dados históricos de ações para um determinado símbolo.

    Args:
        symbol (str): O símbolo da ação para obter dados.

    Returns:
        pandas.DataFrame: Dados processados da ação.
    """
    data = get_stock_data(symbol)
    return process_stock_data(data)

def create_stock_chart(df, symbol):
    """
    Cria um gráfico de linhas para o preço de fechamento e médias móveis de uma ação.

    Args:
        df (pandas.DataFrame): Dados processados da ação.
        symbol (str): O símbolo da ação.

    Returns:
        plotly.graph_objects.Figure: Gráfico de linhas.
    """
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()

    fig = go.Figure()
    
    # Adicionar linha de preço de fechamento
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name='Preço de Fechamento'))

    # Adicionar médias móveis
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['SMA_20'], mode='lines', name='Média Móvel 20'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['SMA_50'], mode='lines', name='Média Móvel 50'))

    # Atualizar layout do gráfico
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
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='rgba(0, 0, 0, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0.8)',
        font_color='white',
        title_font_color='white',
        xaxis_title_font_color='white',
        yaxis_title_font_color='white',
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    return fig

def create_volume_chart(df, symbol):
    """
    Cria um gráfico de barras para o volume de negociação de uma ação.

    Args:
        df (pandas.DataFrame): Dados processados da ação.
        symbol (str): O símbolo da ação.

    Returns:
        plotly.graph_objects.Figure: Gráfico de barras.
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['timestamp'], y=df['volume'], name='Volume'))

    fig.update_layout(
        title=f'Volume de Negociação: {company_names[symbol]}',
        xaxis_title='Tempo',
        yaxis_title='Volume',
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='rgba(0, 0, 0, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0.8)',
        font_color='white',
        title_font_color='white',
        xaxis_title_font_color='white',
        yaxis_title_font_color='white',
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    return fig

def create_open_close_chart(df, symbol):
    """
    Cria um gráfico de linhas para os preços de abertura e fechamento de uma ação.

    Args:
        df (pandas.DataFrame): Dados processados da ação.
        symbol (str): O símbolo da ação.

    Returns:
        plotly.graph_objects.Figure: Gráfico de linhas.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['open'], mode='lines', name='Preço de Abertura'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name='Preço de Fechamento'))

    fig.update_layout(
        title=f'Preço de Abertura e Fechamento: {company_names[symbol]}',
        xaxis_title='Tempo',
        yaxis_title='Preço',
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='rgba(0, 0, 0, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0.8)',
        font_color='white',
        title_font_color='white',
        xaxis_title_font_color='white',
        yaxis_title_font_color='white',
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    return fig

def get_top_10_stocks():
    """
    Obtém os dados das 10 principais ações, classificadas pelo preço de fechamento mais recente.

    Returns:
        list: Uma lista das 10 principais ações com seus dados.
    """
    # Lista de símbolos das ações para monitorar
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NFLX', 'NVDA', 'PYPL', 'ADBE']
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

    return top_stocks[:10]

def get_all_symbols():
    """
    Retorna uma lista de todos os símbolos das ações monitoradas.

    Returns:
        list: Lista de símbolos das ações.
    """
    return company_names.keys()
