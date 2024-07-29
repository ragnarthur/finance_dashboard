import yfinance as yf

def get_top_10_cryptos():
    """
    Obtém os dados das 10 principais criptomoedas por volume.

    Returns:
        list: Uma lista de dicionários contendo informações sobre as 10 principais criptomoedas.
    """
    # Lista de símbolos das 10 principais criptomoedas
    symbols = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'ADA-USD', 'XRP-USD', 'DOGE-USD', 'SOL-USD', 'DOT-USD', 'UNI-USD', 'LTC-USD']
    top_cryptos = []

    # Para cada símbolo na lista de criptomoedas
    for symbol in symbols:
        data = yf.Ticker(symbol)  # Obter dados do ticker usando yfinance
        hist = data.history(period="1d")  # Obter histórico de 1 dia

        # Verificar se o histórico não está vazio
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]  # Obter o preço de fechamento mais recente
            volume = hist['Volume'].iloc[-1]  # Obter o volume mais recente
            opening_price = hist['Open'].iloc[0]  # Obter o preço de abertura do dia
        else:
            current_price = 0  # Se o histórico estiver vazio, definir preço atual como 0
            volume = 0  # Se o histórico estiver vazio, definir volume como 0
            opening_price = 0  # Se o histórico estiver vazio, definir preço de abertura como 0

        # Adicionar as informações da criptomoeda à lista top_cryptos
        top_cryptos.append({
            'id': symbol,
            'symbol': symbol,
            'name': data.info.get('name', symbol),  # Obter o nome da criptomoeda, ou usar o símbolo se não estiver disponível
            'current_price': current_price,
            'total_volume': volume,
            'opening_price': opening_price
        })

    return top_cryptos

def get_crypto_data(symbol):
    """
    Obtém os dados históricos de preço e volume de uma criptomoeda específica.

    Args:
        symbol (str): O símbolo da criptomoeda.

    Returns:
        dict: Um dicionário contendo timestamps, preços de fechamento e volumes da criptomoeda.
    """
    ticker = yf.Ticker(symbol)  # Obter dados do ticker usando yfinance
    hist = ticker.history(period="5d", interval="1h")  # Obter histórico de 5 dias com intervalo de 1 hora

    # Preparar os dados no formato de dicionário
    data = {
        'timestamp': hist.index.tolist(),  # Lista de timestamps
        'price': hist['Close'].tolist(),  # Lista de preços de fechamento
        'volume': hist['Volume'].tolist()  # Lista de volumes
    }
    return data
