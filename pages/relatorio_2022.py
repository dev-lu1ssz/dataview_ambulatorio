from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Relatórios - 2022")

st.title("Relatórios - 2022")
st.text(
    "Visualize exames e atendimentos por especialidade nos três quadrimestres."
)

arquivo_dados = (
    Path(__file__).resolve().parents[1]
    / "databases"
    / "dados_relatorios.xlsx"
)
dados = pd.read_excel(
    arquivo_dados,
    sheet_name="RELATÓRIO QUADRIMESTRAL 2022",
    header=None,
)


def mostrar_grafico(titulo, dados_grafico, titulo_eixo_y):
    mapa_opcoes = {
        0: "1° quadrimestre",
        1: "2° quadrimestre",
        2: "3° quadrimestre",
        3: "Todos",
    }
    selecao = st.pills(
        "Opções",
        options=mapa_opcoes.keys(),
        format_func=lambda opcao: mapa_opcoes[opcao],
        selection_mode="single",
        default=3,
    )

    if selecao is None:
        st.info("Selecione um quadrimestre para visualizar o gráfico.")
        return

    series_por_quadrimestre = {
        0: "1° quadrimestre",
        1: "2° quadrimestre",
        2: "3° quadrimestre",
    }
    if selecao == 3:
        series = list(series_por_quadrimestre.values())
    else:
        series = [series_por_quadrimestre[selecao]]

    st.subheader(titulo)
    tab_grafico, tab_dataframe = st.tabs(["Gráfico de barras", "Dataframe"])
    tab_grafico.bar_chart(
        dados_grafico,
        x="Especialidade",
        y=series,
        horizontal=False,
        width="stretch",
        height=500,
    )
    tab_dataframe.dataframe(
        dados_grafico[["Especialidade", *series]],
        hide_index=True,
        width="stretch",
    )

    especialidade_selecionada = st.selectbox(
        "Selecione uma especialidade para visualizar o desempenho",
        options=dados_grafico["Especialidade"].tolist(),
        key=f"especialidade_{titulo}",
    )
    desempenho_especialidade = dados_grafico.loc[
        dados_grafico["Especialidade"] == especialidade_selecionada
    ].iloc[0]
    desempenho = pd.DataFrame(
        {
            "Quadrimestre": list(series_por_quadrimestre.values()),
            titulo_eixo_y: [
                desempenho_especialidade[nome]
                for nome in series_por_quadrimestre.values()
            ],
        }
    )

    st.subheader(f"Desempenho de {especialidade_selecionada} por quadrimestre")
    col1, col2 = st.columns(2, border=True)
    grafico_pizza = px.pie(
        desempenho,
        names="Quadrimestre",
        values=titulo_eixo_y,
        title="Distribuição por quadrimestre",
    )
    col1.plotly_chart(
        grafico_pizza,
        width="stretch",
    )
    col2.subheader("Valores por quadrimestre")
    col2.dataframe(
        desempenho,
        hide_index=True,
        width="stretch",
    )


def preparar_dados(inicio, fim):
    quadrimestres = {
        "1° quadrimestre": 5,
        "2° quadrimestre": 10,
        "3° quadrimestre": 15,
    }
    dados_grafico = pd.DataFrame(
        {
            "Especialidade": dados.iloc[inicio:fim, 0].astype("string").str.strip(),
            **{
                nome: pd.to_numeric(
                    dados.iloc[inicio:fim, coluna],
                    errors="coerce",
                ).fillna(0).astype(int)
                for nome, coluna in quadrimestres.items()
            },
        }
    )
    return dados_grafico.dropna(subset=["Especialidade"]).reset_index(drop=True)


def relatorio_atendimentos():
    mostrar_grafico(
        "Quantidade de atendimentos por especialidade",
        preparar_dados(7, 24),
        "Atendimentos",
    )


def relatorio_exames():
    mostrar_grafico(
        "Quantidade de exames por especialidade",
        preparar_dados(44, 54),
        "Exames",
    )


opcoes_relatorio = {
    "Relatório de Atendimentos": relatorio_atendimentos,
    "Relatório de Exames": relatorio_exames,
}
relatorio_selecionado = st.selectbox(
    "O que você deseja visualizar?",
    options=opcoes_relatorio.keys(),
)
opcoes_relatorio[relatorio_selecionado]()