import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title='Relatórios')

st.title('Relatórios - 2021')
st.text('Visualize exames, atendimentos e tratamentos terapêuticos por especialidade.')

arquivo_dados = Path(__file__).with_name("relatorio_2021.xlsx")
dados = pd.read_excel(arquivo_dados, sheet_name='RELATÓRIO QUADRIMESTRAL 2021')


def mostrar_grafico(titulo, especialidades, prim_quad, seg_quad, terc_quad):
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

    if selection is None:
        st.info('Selecione um quadrimestre para visualizar o gráfico.')
        return

    series_por_quadrimestre = {
        0: ('1° quadrimestre', prim_quad),
        1: ('2° quadrimestre', seg_quad),
        2: ('3° quadrimestre', terc_quad),
    }

    grafico = pd.DataFrame({'Especialidade': especialidades.to_numpy()})

    if selection == 3:
        for nome, valores in series_por_quadrimestre.values():
            grafico[nome] = valores.to_numpy()
        series = list(grafico.columns[1:])
    else:
        nome, valores = series_por_quadrimestre[selection]
        grafico[nome] = valores.to_numpy()
        series = [nome]

    st.subheader(titulo)
    st.bar_chart(
        grafico,
        x='Especialidade',
        y=series,
        horizontal=False,
        width='stretch',
        height=500
    )


def relatorio_exames():
    especialidades = dados.iloc[39:49, 0].astype(str)
    prim_quad = pd.to_numeric(dados.iloc[39:49, 5], errors='coerce').fillna(0).astype(int)
    seg_quad = pd.to_numeric(dados.iloc[39:49, 10], errors='coerce').fillna(0).astype(int)
    terc_quad = pd.to_numeric(dados.iloc[39:49, 15], errors='coerce').fillna(0).astype(int)

    mostrar_grafico(
        'Quantidade de exames por especialidade',
        especialidades,
        prim_quad,
        seg_quad,
        terc_quad,
    )


def relatorio_atendimentos():
    especialidades = dados.iloc[7:24, 0].astype(str)
    prim_quad = pd.to_numeric(dados.iloc[7:24, 5], errors='coerce').fillna(0).astype(int)
    seg_quad = pd.to_numeric(dados.iloc[7:24, 10], errors='coerce').fillna(0).astype(int)
    terc_quad = pd.to_numeric(dados.iloc[7:24, 15], errors='coerce').fillna(0).astype(int)

    mostrar_grafico(
        'Quantidade de atendimentos por especialidade',
        especialidades,
        prim_quad,
        seg_quad,
        terc_quad,
    )


def relatorio_trat_terapeutico():
    especialidades = dados.iloc[40:47, 22].astype(str)
    prim_quad = pd.to_numeric(dados.iloc[40:47, 27], errors='coerce').fillna(0).astype(int)
    seg_quad = pd.to_numeric(dados.iloc[40:47, 32], errors='coerce').fillna(0).astype(int)
    terc_quad = pd.to_numeric(dados.iloc[40:47, 37], errors='coerce').fillna(0).astype(int)

    mostrar_grafico(
        'Quantidade de tratamentos terapêuticos por especialidade',
        especialidades,
        prim_quad,
        seg_quad,
        terc_quad,
    )


opcoes_relatorio = {
    'Relatório de Exames': relatorio_exames,
    'Atendimentos': relatorio_atendimentos,
    'Tratamentos terapêuticos': relatorio_trat_terapeutico,
}
relatorio_selecionado = st.selectbox(
    'O que você deseja visualizar?',
    options=opcoes_relatorio.keys(),
)
opcoes_relatorio[relatorio_selecionado]()