import os
from flask import Flask, render_template, request, jsonify
from utils.data_fetcher import (
    get_processed_stock_data, create_stock_chart, 
    create_volume_chart, create_open_close_chart,
    get_top_10_stocks, get_all_symbols, company_names
)
from utils.crypto_data_fetcher import get_top_10_cryptos, get_crypto_data
from utils.crypto_chart_generator import (
    create_crypto_charts, create_crypto_pie_chart,
    create_crypto_volume_chart, create_crypto_bar_chart
)
from utils.news_fetcher import get_financial_news
import plotly.express as px
import pandas as pd
import logging
from datetime import datetime, timedelta
import urllib.parse
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar logging para exibir mensagens de depuração
logging.basicConfig(level=logging.DEBUG)

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Obter a API key das variáveis de ambiente
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# Cache para armazenar notícias e evitar consultas repetidas
news_cache = {
    'ações financeiras': {'data': None, 'timestamp': None},
    'criptomoedas': {'data': None, 'timestamp': None}
}
CACHE_EXPIRY = timedelta(minutes=30)  # Definir o tempo de expiração do cache

def get_cached_news(query):
    """Obtém notícias do cache ou faz uma nova solicitação se o cache estiver expirado."""
    current_time = datetime.now()
    cache_key = urllib.parse.quote(query)
    cache = news_cache.get(cache_key, {'data': None, 'timestamp': None})
    
    if cache['data'] is None or current_time - cache['timestamp'] > CACHE_EXPIRY:
        logging.debug(f"Fetching news for query: {query}")
        news_articles = get_financial_news(NEWS_API_KEY, query)
        if news_articles:
            news_cache[cache_key] = {'data': news_articles[:5], 'timestamp': current_time}
        else:
            news_cache[cache_key] = {'data': [], 'timestamp': current_time}
    else:
        logging.debug(f"Using cached news for query: {query}")
    
    return news_cache[cache_key]['data']

@app.route('/')
def index():
    """Rota principal que exibe o dashboard com gráficos e notícias financeiras."""
    try:
        top_stocks = get_top_10_stocks()  # Obter as 10 principais ações
        charts = []
        for stock in top_stocks:
            symbol = stock[0]
            df = get_processed_stock_data(symbol)
            fig = create_stock_chart(df, symbol)
            charts.append(fig.to_html(full_html=False))
        symbols = get_all_symbols()
        news_articles = get_cached_news('ações financeiras')  # Obter notícias financeiras
        return render_template('index.html', charts=charts, top_stocks=top_stocks, symbols=symbols, company_names=company_names, news_articles=news_articles)
    except Exception as e:
        logging.error(f"Erro ao carregar a página inicial: {e}")
        return render_template('error.html', message=str(e))

@app.route('/about')
def about():
    """Rota que exibe a página sobre o projeto."""
    return render_template('about.html')

@app.route('/update_chart', methods=['POST'])
def update_chart():
    """Rota que atualiza os gráficos com base na ação selecionada."""
    symbol = request.form['symbol']
    try:
        df = get_processed_stock_data(symbol)
        fig_price = create_stock_chart(df, symbol)
        fig_volume = create_volume_chart(df, symbol)
        fig_open_close = create_open_close_chart(df, symbol)
        graph_html_price = fig_price.to_html(full_html=False)
        graph_html_volume = fig_volume.to_html(full_html=False)
        graph_html_open_close = fig_open_close.to_html(full_html=False)
        return jsonify({
            'graph_html_price': graph_html_price,
            'graph_html_volume': graph_html_volume,
            'graph_html_open_close': graph_html_open_close
        })
    except ValueError as e:
        logging.error(f"Erro ao atualizar o gráfico para {symbol}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_pie_chart')
def update_pie_chart():
    """Rota que atualiza o gráfico de pizza com as ações principais."""
    try:
        top_stocks = get_top_10_stocks()
        names = [company_names[stock[0]] for stock in top_stocks]
        volumes = [stock[3] for stock in top_stocks]
        df_pie = pd.DataFrame({'Ação': names, 'Volume': volumes, 'Tempo': ['Atual'] * len(names)})
        fig_pie = px.pie(df_pie, names='Ação', values='Volume', title='Distribuição de Volume das Ações Top 10')
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(plot_bgcolor='rgba(0, 0, 0, 0.8)', paper_bgcolor='rgba(0, 0, 0, 0.8)', font_color='white', title_font_color='white')
        graph_html_pie = fig_pie.to_html(full_html=False)
        return jsonify({'graph_html_pie': graph_html_pie})
    except Exception as e:
        logging.error(f"Erro ao atualizar o gráfico de pizza: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_bar_chart')
def update_bar_chart():
    """Rota que atualiza o gráfico de barras com as variações percentuais das ações."""
    try:
        top_stocks = get_top_10_stocks()
        names = [company_names[stock[0]] for stock in top_stocks]
        percent_changes = [stock[4] for stock in top_stocks]
        df_bar = pd.DataFrame({'Ação': names, 'Variação Percentual': percent_changes})
        fig_bar = px.bar(df_bar, x='Ação', y='Variação Percentual', title='Variação Percentual das Top 10 Ações')
        fig_bar.update_traces(textposition='outside')
        fig_bar.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0.8)', 
            paper_bgcolor='rgba(0, 0, 0, 0.8)', 
            font_color='white', 
            title_font_color='white', 
            xaxis_title_font_color='white', 
            yaxis_title_font_color='white', 
            xaxis=dict(showgrid=False, zeroline=False), 
            yaxis=dict(showgrid=False, zeroline=False)
        )
        graph_html_bar = fig_bar.to_html(full_html=False)
        return jsonify({'graph_html_bar': graph_html_bar})
    except Exception as e:
        logging.error(f"Erro ao atualizar o gráfico de barras: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_crypto_chart', methods=['POST'])
def update_crypto_chart():
    """Rota que atualiza os gráficos de criptomoedas com base na criptomoeda selecionada."""
    crypto = request.form['crypto']
    try:
        data = get_crypto_data(crypto)
        df = pd.DataFrame(data)
        fig_price = create_crypto_charts(df, 'price')
        fig_volume = create_crypto_volume_chart(df, 'volume')
        fig_price.update_layout(title="Preço ao longo do tempo")
        fig_volume.update_layout(title="Volume ao longo do tempo")
        graph_html_price = fig_price.to_html(full_html=False)
        graph_html_volume = fig_volume.to_html(full_html=False)
        return jsonify({
            'graph_html_price': graph_html_price,
            'graph_html_volume': graph_html_volume
        })
    except ValueError as e:
        logging.error(f"Erro ao atualizar o gráfico para {crypto}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_crypto_pie_chart')
def update_crypto_pie_chart():
    """Rota que atualiza o gráfico de pizza com as criptomoedas principais."""
    try:
        top_cryptos = get_top_10_cryptos()
        df_pie = pd.DataFrame(top_cryptos)
        fig_pie = create_crypto_pie_chart(df_pie, 'total_volume', 'Distribuição de Volume das Top 10 Criptomoedas')
        graph_html_pie = fig_pie.to_html(full_html=False)
        return jsonify({'graph_html_pie': graph_html_pie})
    except Exception as e:
        logging.error(f"Erro ao atualizar o gráfico de pizza: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_crypto_bar_chart')
def update_crypto_bar_chart():
    """Rota que atualiza o gráfico de barras com os preços atuais das criptomoedas."""
    try:
        top_cryptos = get_top_10_cryptos()
        df_bar = pd.DataFrame({
            'name': [crypto['name'] for crypto in top_cryptos],
            'current_price': [crypto['current_price'] for crypto in top_cryptos]
        })
        fig_bar = create_crypto_bar_chart(df_bar, 'name', 'current_price', 'Preço Atual das Top 10 Criptomoedas')
        graph_html_bar = fig_bar.to_html(full_html=False)
        return jsonify({'graph_html_bar': graph_html_bar})
    except Exception as e:
        logging.error(f"Erro ao atualizar o gráfico de barras: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/cryptos')
def cryptos():
    """Rota que exibe o dashboard de criptomoedas com gráficos e notícias."""
    try:
        top_cryptos = get_top_10_cryptos()
        graph_html_pie = create_crypto_pie_chart(pd.DataFrame(top_cryptos), 'total_volume', 'Distribuição de Volume das Top 10 Criptomoedas')
        df_bar = pd.DataFrame({
            'name': [crypto['name'] for crypto in top_cryptos],
            'current_price': [crypto['current_price'] for crypto in top_cryptos]
        })
        fig_bar = create_crypto_bar_chart(df_bar, 'name', 'current_price', 'Preço Atual das Top 10 Criptomoedas')
        graph_html_bar = fig_bar.to_html(full_html=False)
        news_articles = get_cached_news('criptomoedas')
        return render_template('cryptos.html', top_cryptos=top_cryptos, graph_html_pie=graph_html_pie, graph_html_bar=graph_html_bar, news_articles=news_articles)
    except Exception as e:
        logging.error(f"Erro ao carregar a página de criptomoedas: {e}")
        return render_template('error.html', message=str(e))

if __name__ == '__main__':
    app.run(debug=True)

