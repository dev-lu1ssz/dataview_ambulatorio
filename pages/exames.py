import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title='Relatórios de exames')

st.title('Relatórios de Exames - 2021')
st.text('Dados de exames realizados no ano de 2021 separados por quadrimestre (1°, 2° e 3°)')

arquivo_dados = Path(__file__).with_name("relatorio_2021.xlsx")
dados = pd.read_excel(arquivo_dados, sheet_name='RELATÓRIO QUADRIMESTRAL 2021')

especialidades_medicas = dados.iloc[39:49, 0].astype(str)
prim_quad = pd.to_numeric(dados.iloc[39:49, 5], errors='coerce').fillna(0).astype(int)
seg_quad = pd.to_numeric(dados.iloc[39:49, 10], errors='coerce').fillna(0).astype(int)
terc_quad = pd.to_numeric(dados.iloc[39:49, 15], errors='coerce').fillna(0).astype(int)

mapa_opcoes = {
    0: '1° quadrimestre',
    1: '2° quadrimestre',
    2: '3° quadrimestre',
    3: 'Todos'
}
selection = st.pills(
    'Opções',
    options=mapa_opcoes.keys(),
    format_func=lambda option: mapa_opcoes[option],
    selection_mode='single',
    default=3,
)

series_por_quadrimestre = {
    0: ('1° quadrimestre', prim_quad),
    1: ('2° quadrimestre', seg_quad),
    2: ('3° quadrimestre', terc_quad),
}

grafico = pd.DataFrame({'Especialidade': especialidades_medicas.to_numpy()})

if selection == 3:
    for nome, valores in series_por_quadrimestre.values():
        grafico[nome] = valores.to_numpy()
    series = list(grafico.columns[1:])
else:
    nome, valores = series_por_quadrimestre[selection]
    grafico[nome] = valores.to_numpy()
    series = [nome]

st.subheader('Quantidade de exames por especialidade')
st.bar_chart(
    grafico,
    x='Especialidade',
    y=series,
    horizontal=False,
    width='stretch'
)
