# FinanVision - Dashboard de Análise Financeira

---

#### Índice

1. [Visão Geral](#visão-geral)
2. [Funcionalidades](#funcionalidades)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Instalação](#instalação)
5. [Uso](#uso)
6. [Rotas Disponíveis](#rotas-disponíveis)
7. [Sobre a Equipe](#sobre-a-equipe)
8. [Contato](#contato)
9. [Licença](#licença)
10. [Download](#download)

---

### Visão Geral

FinanVision é um dashboard abrangente desenvolvido para fornecer uma visão completa das principais ações e criptomoedas do mercado financeiro. Ele utiliza dados em tempo real para ajudar investidores e entusiastas a tomar decisões informadas. O dashboard também apresenta notícias financeiras atualizadas automaticamente, garantindo que os usuários estejam sempre cientes das últimas tendências do mercado.

---

### Funcionalidades

- **Visualização de Dados de Ações**: Gráficos interativos de preço, volume e variação percentual das top 10 ações.
- **Visualização de Dados de Criptomoedas**: Gráficos interativos de preço e volume das top 10 criptomoedas.
- **Notícias Financeiras**: Exibição de notícias atualizadas sobre ações e criptomoedas.
- **Interface Intuitiva**: Design moderno e responsivo com fácil navegação.
- **Cache de Notícias**: Cache de notícias para evitar repetição e garantir variedade nas notícias apresentadas.

---

### Tecnologias Utilizadas

- **Frontend**: HTML, CSS (Bootstrap), JavaScript (jQuery)
- **Backend**: Python (Flask)
- **Bibliotecas Python**: 
  - `requests` para chamadas de API
  - `plotly` para criação de gráficos interativos
  - `pandas` para manipulação de dados
- **APIs**:
  - `Alpha Vantage` para dados financeiros
  - `newsapi` para notícias financeiras

---

### Instalação

1. **Clone o Repositório**
    ```sh
    git clone https://github.com/seu-usuario/finanvision.git
    cd finanvision
    ```

2. **Crie e Ative um Ambiente Virtual**
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. **Instale as Dependências**
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure as Chaves da API**
    - Crie um arquivo `.env` na raiz do projeto e adicione suas chaves da API:
    ```env
    ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
    NEWS_API_KEY=your_news_api_key
    ```

---

### Uso

1. **Inicie o Servidor Flask**
    ```sh
    flask run
    ```

2. **Acesse o Dashboard**
    - Abra seu navegador e acesse `http://127.0.0.1:5000`

---

### Rotas Disponíveis

- **Rota Principal**
  - **URL**: `/`
  - **Descrição**: Exibe o dashboard principal com dados de ações e notícias relacionadas.

- **Rota de Criptomoedas**
  - **URL**: `/cryptos`
  - **Descrição**: Exibe o dashboard de criptomoedas com dados das principais moedas digitais e notícias relacionadas.

- **Rota Sobre**
  - **URL**: `/about`
  - **Descrição**: Exibe informações sobre o FinanVision e a equipe de desenvolvimento.

---


### Contato

- **E-mail**: [arthuraraujo07@hotmail.com](mailto:arthuraraujo07@hotmail.com)
- **GitHub**: [github.com/seu-usuario](https://github.com/seu-usuario)

---

### Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

### Download

Você pode baixar o FinanVision diretamente do nosso [repositório GitHub](https://github.com/seu-usuario/finanvision).

---

Sinta-se à vontade para contribuir com o projeto abrindo issues e pull requests. Agradecemos seu interesse e esperamos que o FinanVision seja uma ferramenta útil para suas análises financeiras.
