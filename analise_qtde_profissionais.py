from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Painel de dados")


def mostrar_profissionais():
    st.image('pedro_ernesto.jpeg', caption='Hospital Universitário Pedro Ernesto', alt='Imagem do HUPE') # Adicionar imagem
    st.title('Dados do ambulatório') # Título da página
    st.text('Base de dados simples, sem grandes informações, que mostram a quantidade de profisionais em cada setor. Veja o gráfico comparativo e use a caixa de seleção para visualizar cada ano de 2021-2024')
    st.markdown("#### Profissionais do ambulatório - Especialidade médica")
    arquivo_dados = Path(__file__).with_name("qtde_profissionais.xlsx")
    dados = pd.read_excel(arquivo_dados, header=None, skiprows=2, usecols=range(5))

    anos = ["2021", "2022", "2023", "2024"]
    dados.columns = ["Especialidade", *anos]
    dados = dados.dropna(subset=["Especialidade"]).copy()
    dados[anos] = dados[anos].apply(pd.to_numeric).astype("int64")

    ano_selecionado = st.selectbox(
        "Selecione o ano que deseja visualizar",
        options=anos,
    )

    grafico = dados[["Especialidade", ano_selecionado]]

    st.subheader(f"Quantidade de profissionais por setor em {ano_selecionado}")
    st.bar_chart(
        grafico,
        x="Especialidade",
        y=ano_selecionado,
        horizontal=False,
        width='stretch'
    )

    st.markdown("#### Profissionais do ambulatório - Especialidade não médica")
    dados_nao_medicos = pd.read_excel(
        arquivo_dados,
        sheet_name="Planilha3",
        header=None,
        skiprows=2,
        usecols="D:E",
    )
    dados_nao_medicos.columns = ["Especialidade", "Quantidade"]
    dados_nao_medicos = dados_nao_medicos.dropna(
        subset=["Especialidade", "Quantidade"]
    ).copy()
    dados_nao_medicos["Quantidade"] = pd.to_numeric(
        dados_nao_medicos["Quantidade"]
    ).astype("int64")
    dados_nao_medicos = dados_nao_medicos.loc[
        ~dados_nao_medicos["Especialidade"].str.startswith(
            "TOTAL DE PROFISSIONAIS", na=False
        )
    ]

    st.bar_chart(
        dados_nao_medicos,
        x="Especialidade",
        y="Quantidade",
        sort=True
    )


exames_page = st.Page("pages/relatorios.py", title="Relatórios", icon="📜")
navigation = st.navigation(
    [
        st.Page(
            mostrar_profissionais,
            title="QTDE Profissionais",
            icon="📊",
            default=True,
        ),
        exames_page,
    ]
)
navigation.run()
