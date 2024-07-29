import plotly.express as px

def create_crypto_pie_chart(df, value_column, title):
    """
    Cria um gráfico de pizza para exibir a distribuição de um valor específico entre diferentes criptomoedas.

    Args:
        df (DataFrame): DataFrame contendo os dados das criptomoedas.
        value_column (str): Nome da coluna no DataFrame que contém os valores a serem plotados.
        title (str): Título do gráfico.

    Returns:
        Figure: Um objeto Plotly Figure contendo o gráfico de pizza.
    """
    fig = px.pie(df, names='name', values=value_column, title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.8)', 
        paper_bgcolor='rgba(0, 0, 0, 0.8)', 
        font_color='white', 
        title_font_color='white'
    )
    return fig

def create_crypto_bar_chart(df, x_column, y_column, title):
    """
    Cria um gráfico de barras para exibir os valores de uma coluna específica para diferentes criptomoedas.

    Args:
        df (DataFrame): DataFrame contendo os dados das criptomoedas.
        x_column (str): Nome da coluna no DataFrame para o eixo x.
        y_column (str): Nome da coluna no DataFrame para o eixo y.
        title (str): Título do gráfico.

    Returns:
        Figure: Um objeto Plotly Figure contendo o gráfico de barras.
    """
    fig = px.bar(df, x=x_column, y=y_column, title=title)
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0.8)',
        font_color='white',
        title_font_color='white',
        xaxis_title_font_color='white',
        yaxis_title_font_color='white',
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )
    return fig

def create_crypto_line_chart(df):
    """
    Cria um gráfico de linhas para exibir o preço de abertura das principais criptomoedas.

    Args:
        df (DataFrame): DataFrame contendo os dados das criptomoedas.

    Returns:
        Figure: Um objeto Plotly Figure contendo o gráfico de linhas.
    """
    df = df.rename(columns={'name': 'Nome', 'opening_price': 'Preço de Abertura'})
    fig = px.line(df, x='Nome', y='Preço de Abertura', title='Preço de Abertura das Top 10 Criptomoedas')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.8)', 
        paper_bgcolor='rgba(0, 0, 0, 0.8)', 
        font_color='white', 
        title_font_color='white'
    )
    return fig

def create_crypto_charts(df, column_name):
    """
    Cria um gráfico de linhas para exibir a variação de um valor específico ao longo do tempo.

    Args:
        df (DataFrame): DataFrame contendo os dados das criptomoedas.
        column_name (str): Nome da coluna no DataFrame para plotar no eixo y.

    Returns:
        Figure: Um objeto Plotly Figure contendo o gráfico de linhas.
    """
    column_label = 'Preço' if column_name == 'price' else column_name.capitalize()
    fig = px.line(df, x='timestamp', y=column_name, title=f'{column_label} ao longo do tempo')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.8)', 
        paper_bgcolor='rgba(0, 0, 0, 0.8)', 
        font_color='white', 
        title_font_color='white'
    )
    return fig

def create_crypto_volume_chart(df, column_name):
    """
    Cria um gráfico de barras para exibir o volume de transações de uma criptomoeda ao longo do tempo.

    Args:
        df (DataFrame): DataFrame contendo os dados das criptomoedas.
        column_name (str): Nome da coluna no DataFrame para plotar no eixo y.

    Returns:
        Figure: Um objeto Plotly Figure contendo o gráfico de barras.
    """
    column_label = 'Volume' if column_name == 'volume' else column_name.capitalize()
    fig = px.bar(df, x='timestamp', y=column_name, title=f'{column_label} ao longo do tempo')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.8)', 
        paper_bgcolor='rgba(0, 0, 0, 0.8)', 
        font_color='white', 
        title_font_color='white'
    )
    return fig
