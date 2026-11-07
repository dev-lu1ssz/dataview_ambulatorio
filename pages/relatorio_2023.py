import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title='Relatórios - 2023')

st.title('Relatórios - 2023')
st.text('Visualize exames, atendimentos e tratamentos terapêuticos por especialidade.')

arquivo_dados = (
    Path(__file__).resolve().parents[1]
    / "databases"
    / "dados_relatorios.xlsx"
)

dados = pd.read_excel(arquivo_dados, sheet_name='RELATÓRIO QUADRIMESTRAL 2023')

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

    especialidade_selecionada = st.selectbox(
        'Selecione uma especialidade para visualizar o desempenho',
        options=especialidades.tolist(),
    )
    indice_especialidade = especialidades[
        especialidades == especialidade_selecionada
    ].index[0]
    desempenho = pd.DataFrame(
        {
            'Quadrimestre': [
                '1° quadrimestre',
                '2° quadrimestre',
                '3° quadrimestre',
            ],
            'Total': [
                prim_quad.loc[indice_especialidade],
                seg_quad.loc[indice_especialidade],
                terc_quad.loc[indice_especialidade],
            ],
        }
    )

    st.subheader(f'Desempenho de {especialidade_selecionada} por quadrimestre')
    col1, col2 = st.columns(2, border=True)

    grafico_pizza = px.pie(
        desempenho,
        names='Quadrimestre',
        values='Total',
        title='Distribuição por quadrimestre',
    )
    col1.plotly_chart(
        grafico_pizza,
        width='stretch',
    )

    col2.subheader('Valores por quadrimestre')
    col2.dataframe(
        desempenho,
        hide_index=True,
        width='stretch',
    )


def relatorio_exames():
    especialidades = dados.iloc[44:54, 0].astype(str)  # Eixo X (embaixo do gráfico)
    prim_quad = pd.to_numeric(dados.iloc[44:54, 5], errors='coerce').fillna(0).astype(int)
    seg_quad = pd.to_numeric(dados.iloc[44:54, 10], errors='coerce').fillna(0).astype(int)
    terc_quad = pd.to_numeric(dados.iloc[44:54, 15], errors='coerce').fillna(0).astype(int)

    mostrar_grafico(
        'Quantidade de exames por especialidade',
        especialidades,
        prim_quad,
        seg_quad,
        terc_quad,
    )


def relatorio_atendimentos():
    especialidades = dados.iloc[7:29, 0].astype(str)
    prim_quad = pd.to_numeric(dados.iloc[7:29, 5], errors='coerce').fillna(0).astype(int)
    seg_quad = pd.to_numeric(dados.iloc[7:29, 10], errors='coerce').fillna(0).astype(int)
    terc_quad = pd.to_numeric(dados.iloc[7:29, 15], errors='coerce').fillna(0).astype(int)

    mostrar_grafico(
        'Quantidade de atendimentos por especialidade',
        especialidades,
        prim_quad,
        seg_quad,
        terc_quad,
    )


def relatorio_trat_terapeutico():
    especialidades = dados.iloc[45:52, 23].astype(str)
    prim_quad = pd.to_numeric(dados.iloc[45:52, 28], errors='coerce').fillna(0).astype(int)
    seg_quad = pd.to_numeric(dados.iloc[45:52, 33], errors='coerce').fillna(0).astype(int)
    terc_quad = pd.to_numeric(dados.iloc[45:52, 38], errors='coerce').fillna(0).astype(int)

    mostrar_grafico(
        'Quantidade de tratamentos terapêuticos por especialidade',
        especialidades,
        prim_quad,
        seg_quad,
        terc_quad,
    )


opcoes_relatorio = {
    'Relatório de Exames': relatorio_exames,
    'Relatório de Atendimentos': relatorio_atendimentos,
    'Relatório de Tratamentos terapêuticos': relatorio_trat_terapeutico,
}
relatorio_selecionado = st.selectbox(
    'O que você deseja visualizar?',
    options=opcoes_relatorio.keys(),
)
opcoes_relatorio[relatorio_selecionado]()