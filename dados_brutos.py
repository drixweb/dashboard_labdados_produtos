import streamlit as st
import pandas as pd
from dashboard import dados
import time

@st.cache_data
def converter_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso!')
    time.sleep(5)
    sucesso.empty()

# Configurações de página
st.set_page_config(
    page_title='Dados Brutos',
    page_icon=':bar_chart:',
    layout='wide'
)

st.title(':bar_chart: DASDOS BRUTOS')

# url = 'https://labdados.com/produtos'
# response = requests.get(url)
# dados = pd.DataFrame.from_dict(response.json())
# dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect(
        'Selecione as Colunas',
        list(dados.columns),
        list(dados.columns)
    )

st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do Produto'):
    produtos = st.multiselect(
        'Selecione os Produtos',
        dados['Produto'].unique(),
        dados['Produto'].unique()
    )
with st.sidebar.expander('Nome da Categoria'):
    categoria = st.multiselect(
        'Selecione as categorias',
        dados['Categoria do Produto'].unique(),
        dados['Categoria do Produto'].unique()
    )
with st.sidebar.expander('Preço do Produto'):
    preco = st.slider(
        'Selecione o Preço',
        0, 5000, (0,5000)
    )
with st.sidebar.expander('Valor do Frete'):
    frete = st.slider(
        'Selecione o valor do Frete',
        0, 250, (0,250)
    )
with st.sidebar.expander('Data da Compra'):
    data_compra = st.date_input(
        'Selecione a data',
        (dados['Data da Compra'].min(), dados['Data da Compra'].max())
    )
with st.sidebar.expander('Vendedor'):
    vendedor = st.multiselect(
        'Selecione os Vendedores',
        dados['Vendedor'].unique(),
        dados['Vendedor'].unique()
    )
with st.sidebar.expander('Local da Compra'):
    local_da_compra = st.multiselect(
        'Selecione os Estados',
        dados['Local da compra'].unique(),
        dados['Local da compra'].unique()
    )
with st.sidebar.expander('Avaliação'):
    avaliacao = st.slider(
        'Selecione a Avaliação',
        1, 5, (1,5)
    )
with st.sidebar.expander('Tipo de Pagamento'):
    pagamento = st.multiselect(
        'Selecione os Tipos de Pagamento',
        dados['Tipo de pagamento'].unique(),
        dados['Tipo de pagamento'].unique()
    )
with st.sidebar.expander('Qtd. Parcelas'):
    parcelas = st.slider(
        'Qtd. de Parcelas',
        1, 24, (1,24)
    )

query = '''
Produto in @produtos and \
`Categoria do Produto` in @categoria and \
@preco[0] <= Preço <= @preco[1] and \
@frete[0] <= Frete <= @frete[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
Vendedor in @vendedor and \
`Local da compra` in @local_da_compra and \
@avaliacao[0] <= `Avaliação da compra` <= @avaliacao[1] and \
`Tipo de pagamento` in @pagamento and \
@parcelas[0] <= `Quantidade de parcelas` <= @parcelas[1]
'''
dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]


st.dataframe(dados_filtrados)
st.markdown(f'Tabela: :blue[{dados_filtrados.shape[0]} x {dados_filtrados.shape[1]}]')

st.markdown('Nome do arquivo')
col_1, col_2 = st.columns(2)
with col_1:
    nome_arquivo = st.text_input('', label_visibility='collapsed')
    nome_arquivo += '.csv'
with col_2:
    st.download_button(
        'Baixar',
        data=converter_csv(dados_filtrados),
        file_name=nome_arquivo,
        mime='text/csv',
        on_click=mensagem_sucesso
    )