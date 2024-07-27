import requests

def get_financial_news(api_key, query):
    url = f"https://newsapi.org/v2/everything?q={query}&language=pt&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and 'articles' in data:
            return data['articles']
    return []

