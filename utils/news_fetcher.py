import requests

def get_financial_news(api_key, query):
    """
    Obtém notícias financeiras com base em uma consulta específica.

    Args:
        api_key (str): A chave de API para acessar o serviço de notícias.
        query (str): A consulta de pesquisa para obter notícias financeiras.

    Returns:
        list: Uma lista de artigos de notícias se a solicitação for bem-sucedida, caso contrário, uma lista vazia.
    """
    # Construir a URL para a API de notícias, incluindo a chave de API e a consulta de pesquisa
    url = f"https://newsapi.org/v2/everything?q={query}&language=pt&apiKey={api_key}"
    
    # Fazer a solicitação HTTP GET para a API de notícias
    response = requests.get(url)
    
    # Verificar se a solicitação foi bem-sucedida (status code 200)
    if response.status_code == 200:
        # Converter a resposta JSON em um dicionário Python
        data = response.json()
        
        # Verificar se os dados contêm a chave 'articles'
        if data and 'articles' in data:
            # Retornar a lista de artigos
            return data['articles']
    
    # Retornar uma lista vazia se a solicitação não for bem-sucedida ou se não houver artigos
    return []
