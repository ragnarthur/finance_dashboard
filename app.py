from flask import Flask, render_template
from utils.data_fetcher import get_processed_stock_data, create_stock_chart

app = Flask(__name__)

@app.route('/')
def index():
    df = get_processed_stock_data('AAPL')
    fig = create_stock_chart(df)
    graph_html = fig.to_html(full_html=False)
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
