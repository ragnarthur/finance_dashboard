from flask import Flask, render_template, request, jsonify
from utils.data_fetcher import (
    get_processed_stock_data, create_stock_chart, 
    create_volume_chart, create_open_close_chart,
    get_top_10_stocks, get_all_symbols, company_names
)
from utils.crypto_data_fetcher import get_top_10_cryptos
from utils.crypto_chart_generator import (
    create_crypto_charts, create_crypto_pie_chart,
    create_crypto_volume_chart, create_crypto_open_close_chart
)
import plotly.express as px
import pandas as pd
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index():
    try:
        top_stocks = get_top_10_stocks()
        charts = []
        for stock in top_stocks:
            symbol = stock[0]
            df = get_processed_stock_data(symbol)
            fig = create_stock_chart(df, symbol)
            charts.append(fig.to_html(full_html=False))
        symbols = get_all_symbols()
        return render_template('index.html', charts=charts, top_stocks=top_stocks, symbols=symbols, company_names=company_names)
    except Exception as e:
        logging.error(f"Erro ao carregar a página inicial: {e}")
        return render_template('error.html', message=str(e))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/update_chart', methods=['POST'])
def update_chart():
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
    try:
        top_stocks = get_top_10_stocks()
        logging.debug(f"Top stocks: {top_stocks}")
        names = [company_names[stock[0]] for stock in top_stocks]
        volumes = [stock[3] for stock in top_stocks]
        df_pie = pd.DataFrame({'Ação': names, 'Volume': volumes, 'Tempo': ['Atual'] * len(names)})
        logging.debug(f"DataFrame para gráfico de pizza: {df_pie}")
        fig_pie = px.pie(df_pie, names='Ação', values='Volume', title='Distribuição de Volume das Ações Top 10')
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0.8)', 
            paper_bgcolor='rgba(0, 0, 0, 0.8)', 
            font_color='white', 
            title_font_color='white'
        )
        graph_html_pie = fig_pie.to_html(full_html=False)
        return jsonify({'graph_html_pie': graph_html_pie})
    except Exception as e:
        logging.error(f"Erro ao atualizar o gráfico de pizza: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_bar_chart')
def update_bar_chart():
    try:
        top_stocks = get_top_10_stocks()
        logging.debug(f"Top stocks: {top_stocks}")
        names = [company_names[stock[0]] for stock in top_stocks]
        percent_changes = [stock[4] for stock in top_stocks]
        df_bar = pd.DataFrame({'Ação': names, 'Variação Percentual': percent_changes})
        logging.debug(f"DataFrame para gráfico de barras: {df_bar}")
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
    crypto = request.form['crypto']
    try:
        top_cryptos = get_top_10_cryptos()
        selected_crypto = next(item for item in top_cryptos if item['id'] == crypto)
        name = selected_crypto['name']
        # Dados fictícios para demonstração
        data = {'timestamp': pd.date_range(start='2023-01-01', periods=50, freq='H'), 'open': pd.Series(range(50)), 'close': pd.Series(range(1, 51)), 'volume': pd.Series(range(100, 150))}
        df = pd.DataFrame(data)
        fig_price = create_crypto_open_close_chart(df, name)
        fig_volume = create_crypto_volume_chart(df, name)
        fig_open_close = create_crypto_open_close_chart(df, name)
        graph_html_price = fig_price.to_html(full_html=False)
        graph_html_volume = fig_volume.to_html(full_html=False)
        graph_html_open_close = fig_open_close.to_html(full_html=False)
        return jsonify({'graph_html_price': graph_html_price, 'graph_html_volume': graph_html_volume, 'graph_html_open_close': graph_html_open_close})
    except ValueError as e:
        logging.error(f"Erro ao atualizar o gráfico para {crypto}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_crypto_pie_chart')
def update_crypto_pie_chart():
    try:
        top_cryptos = get_top_10_cryptos()
        df_pie = pd.DataFrame(top_cryptos)
        fig_pie = create_crypto_pie_chart(df_pie)
        graph_html_pie = fig_pie.to_html(full_html=False)
        return jsonify({'graph_html_pie': graph_html_pie})
    except Exception as e:
        logging.error(f"Erro ao atualizar o gráfico de pizza: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_crypto_bar_chart')
def update_crypto_bar_chart():
    try:
        top_cryptos = get_top_10_cryptos()
        df_bar = pd.DataFrame({'name': [crypto['name'] for crypto in top_cryptos], 'price_change_percentage_24h': [crypto['price_change_percentage_24h'] for crypto in top_cryptos]})
        fig_bar = px.bar(df_bar, x='name', y='price_change_percentage_24h', title='Variação Percentual de Preço das Top 10 Criptomoedas (24h)')
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

@app.route('/cryptos')
def cryptos():
    try:
        top_cryptos = get_top_10_cryptos()
        graph_html_pie = create_crypto_pie_chart(pd.DataFrame(top_cryptos))
        return render_template('cryptos.html', top_cryptos=top_cryptos, graph_html_pie=graph_html_pie)
    except Exception as e:
        logging.error(f"Erro ao carregar a página de criptomoedas: {e}")
        return render_template('error.html', message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
