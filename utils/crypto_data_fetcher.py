import requests

def get_top_10_cryptos():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=params)
    data = response.json()

    top_cryptos = []
    for crypto in data:
        top_cryptos.append({
            'id': crypto['id'],
            'symbol': crypto['symbol'].upper(),
            'name': crypto['name'],
            'current_price': crypto['current_price'],
            'market_cap': crypto['market_cap'],
            'total_volume': crypto['total_volume'],  # Adicionado volume de mercado
            'price_change_percentage_24h': crypto['price_change_percentage_24h']
        })

    return top_cryptos
