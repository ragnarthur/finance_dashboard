from flask import Flask, render_template, request, jsonify
from utils.data_fetcher import (
    get_processed_stock_data, create_stock_chart, 
    create_volume_chart, create_open_close_chart,
    get_top_5_stocks, get_all_symbols, company_names
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
        # Obtenha a lista das top 5 ações
        top_stocks = get_top_5_stocks()

        # Crie gráficos para as top 5 ações
        charts = []
        for stock in top_stocks:
            symbol = stock[0]
            df = get_processed_stock_data(symbol)
            fig = create_stock_chart(df, symbol)
            charts.append(fig.to_html(full_html=False))

        # Obtenha todos os símbolos disponíveis
        symbols = get_all_symbols()

        return render_template('index.html', charts=charts, top_stocks=top_stocks, symbols=symbols, company_names=company_names)
    except Exception as e:
        logging.error(f"Erro ao carregar a página inicial: {e}")
        return render_template('error.html', message=str(e))

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
        top_stocks = get_top_5_stocks()
        logging.debug(f"Top stocks: {top_stocks}")

        names = [company_names[stock[0]] for stock in top_stocks]
        volumes = [stock[3] for stock in top_stocks]
        
        df_pie = pd.DataFrame({
            'Ação': names,
            'Volume': volumes,
            'Tempo': ['Atual'] * len(names)
        })
        logging.debug(f"DataFrame para gráfico de pizza: {df_pie}")

        fig_pie = px.pie(df_pie, names='Ação', values='Volume', title='Distribuição de Volume das Ações Top 5')
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')

        graph_html_pie = fig_pie.to_html(full_html=False)
        return jsonify({'graph_html_pie': graph_html_pie})
    except Exception as e:
        logging.error(f"Erro ao atualizar o gráfico de pizza: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_bar_chart')
def update_bar_chart():
    try:
        top_stocks = get_top_5_stocks()
        logging.debug(f"Top stocks: {top_stocks}")

        names = [company_names[stock[0]] for stock in top_stocks]
        percent_changes = [stock[4] for stock in top_stocks]

        df_bar = pd.DataFrame({
            'Ação': names,
            'Variação Percentual': percent_changes
        })
        logging.debug(f"DataFrame para gráfico de barras: {df_bar}")

        fig_bar = px.bar(df_bar, x='Ação', y='Variação Percentual', title='Variação Percentual das Top 5 Ações')
        fig_bar.update_traces(textposition='outside')

        graph_html_bar = fig_bar.to_html(full_html=False)
        return jsonify({'graph_html_bar': graph_html_bar})
    except Exception as e:
        logging.error(f"Erro ao atualizar o gráfico de barras: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
