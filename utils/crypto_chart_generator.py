import plotly.express as px

def create_crypto_pie_chart(df, value_column, title):
    fig = px.pie(df, names='name', values=value_column, title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.8)', 
        paper_bgcolor='rgba(0, 0, 0, 0.8)', 
        font_color='white', 
        title_font_color='white'
    )
    return fig

def create_crypto_line_chart(df):
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
    fig = px.line(df, x='timestamp', y=column_name, title=f'{column_name.capitalize()} ao longo do tempo')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.8)', 
        paper_bgcolor='rgba(0, 0, 0, 0.8)', 
        font_color='white', 
        title_font_color='white'
    )
    return fig

def create_crypto_volume_chart(df, column_name):
    fig = px.bar(df, x='timestamp', y=column_name, title=f'{column_name.capitalize()} ao longo do tempo')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.8)', 
        paper_bgcolor='rgba(0, 0, 0, 0.8)', 
        font_color='white', 
        title_font_color='white'
    )
    return fig
