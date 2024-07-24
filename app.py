from flask import Flask, render_template
from utils.data_fetcher import get_processed_stock_data, create_stock_chart, get_top_5_stocks

app = Flask(__name__)

@app.route('/')
def index():
    # Obtenha a lista das top 5 ações
    top_stocks = get_top_5_stocks()

    # Crie gráficos para as top 5 ações
    charts = []
    for stock in top_stocks:
        symbol = stock[0]
        df = get_processed_stock_data(symbol)
        fig = create_stock_chart(df, symbol)
        charts.append(fig.to_html(full_html=False))

    return render_template('index.html', charts=charts, top_stocks=top_stocks)

if __name__ == '__main__':
    app.run(debug=True)
