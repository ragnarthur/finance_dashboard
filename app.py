from flask import Flask, render_template, request, jsonify
from utils.data_fetcher import get_processed_stock_data, create_stock_chart, get_top_5_stocks, get_all_symbols, company_names

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
        return render_template('error.html', message=str(e))

@app.route('/update_chart', methods=['POST'])
def update_chart():
    symbol = request.form['symbol']
    try:
        df = get_processed_stock_data(symbol)
        fig = create_stock_chart(df, symbol)
        graph_html = fig.to_html(full_html=False)
        return jsonify({'graph_html': graph_html})
    except ValueError as e:
        app.logger.error(f"Erro ao atualizar o gráfico para {symbol}: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
