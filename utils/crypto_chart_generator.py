import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_crypto_charts(top_cryptos):
    df_cryptos = pd.DataFrame(top_cryptos)
    
    fig_market_cap = px.bar(df_cryptos, x='name', y='market_cap', title='Market Cap das Top 10 Criptomoedas')
    fig_market_cap.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0.8)',
        font_color='white',
        title_font_color='white',
        xaxis_title_font_color='white',
        yaxis_title_font_color='white',
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    fig_price_change = px.bar(df_cryptos, x='name', y='price_change_percentage_24h', title='Variação Percentual de Preço das Top 10 Criptomoedas (24h)')
    fig_price_change.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0.8)',
        font_color='white',
        title_font_color='white',
        xaxis_title_font_color='white',
        yaxis_title_font_color='white',
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )
    
    graph_html_market_cap = fig_market_cap.to_html(full_html=False)
    graph_html_price_change = fig_price_change.to_html(full_html=False)

    return graph_html_market_cap, graph_html_price_change

def create_crypto_pie_chart(df):
    fig_pie = px.pie(df, names='name', values='market_cap', title='Distribuição de Market Cap das Top 10 Criptomoedas')
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0.8)',
        font_color='white',
        title_font_color='white'
    )
    return fig_pie.to_html(full_html=False)

def create_crypto_volume_chart(df, name):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['timestamp'], y=df['volume'], name='Volume'))

    fig.update_layout(
        title=f'Volume de Negociação: {name}',
        xaxis_title='Tempo',
        yaxis_title='Volume',
        margin=dict(l=40, r=40, t=40, b=40),
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

def create_crypto_open_close_chart(df, name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['open'], mode='lines', name='Preço de Abertura'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name='Preço de Fechamento'))

    fig.update_layout(
        title=f'Preço de Abertura e Fechamento: {name}',
        xaxis_title='Tempo',
        yaxis_title='Preço',
        margin=dict(l=40, r=40, t=40, b=40),
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
