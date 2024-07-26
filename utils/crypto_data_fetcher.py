import yfinance as yf

def get_top_10_cryptos():
    symbols = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'ADA-USD', 'XRP-USD', 'DOGE-USD', 'SOL-USD', 'DOT-USD', 'UNI-USD', 'LTC-USD']
    top_cryptos = []

    for symbol in symbols:
        data = yf.Ticker(symbol)
        hist = data.history(period="1d")
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            volume = hist['Volume'].iloc[-1]
            opening_price = hist['Open'].iloc[0]
        else:
            current_price = 0
            volume = 0
            opening_price = 0

        top_cryptos.append({
            'id': symbol,
            'symbol': symbol,
            'name': data.info.get('name', symbol),
            'current_price': current_price,
            'total_volume': volume,
            'opening_price': opening_price
        })

    return top_cryptos

def get_crypto_data(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="5d", interval="1h")
    data = {
        'timestamp': hist.index.tolist(),
        'price': hist['Close'].tolist(),
        'volume': hist['Volume'].tolist()
    }
    return data
