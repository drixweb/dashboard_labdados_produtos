import streamlit as st

home = st.Page(
    'dashboard.py',
    title='Dashboard'
)

dados_brutos = st.Page(
    'dados_brutos.py',
    title='Dados Brutos'
)

pg = st.navigation([home, dados_brutos])


pg.run()