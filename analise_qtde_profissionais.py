from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Painel de dados")


def mostrar_profissionais():
#    st.title('Hospital Universitário Pedro Ernesto')
#    st.image('pedro_ernesto.jpeg', caption='Imagem da área externa') # Adicionar imagem
#    st.text('O Hospital Universitário Pedro Ernesto (HUPE) é o hospital universitário da Universidade do Estado do Rio de Janeiro (UERJ). Foi inaugurado no ano de 1950, sendo parte da rede hospitalar da Secretaria de Saúde do então Distrito Federal. Em 1962 passou a integrar a Universidade do Estado da Guanabara (UEG), que mais tarde se tornaria a UERJ.')
    st.markdown('## Dados do ambulatório') # Título da página
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

    quantidade_maxima = st.slider(
        "Quantidade máxima de profissionais por especialidade",
        min_value=0,
        max_value=int(dados[anos].max().max()),
        value=int(dados[anos].max().max()),
        step=1,
    )
    grafico = dados.loc[
        dados[ano_selecionado] <= quantidade_maxima,
        ["Especialidade", ano_selecionado],
    ]

    st.subheader(f"Quantidade de profissionais por setor em {ano_selecionado}")
    st.bar_chart(
        grafico,
        x="Especialidade",
        y=ano_selecionado,
        horizontal=True,
        width=1200
    )

    st.markdown("#### Profissionais médicos por tipo de vínculo")
    dados_nominais = pd.read_excel(
        arquivo_dados,
        sheet_name="NOMINAL",
        skiprows=1,
        nrows=59,
        usecols=range(4),
    )
    dados_nominais.columns = [
        "ESPECIALIDADE",
        "NOME",
        "TIPO DE VÍNCULO",
        "QUANTIDADE POR ESPECIALIDADE",
    ]
    dados_nominais["QUANTIDADE POR ESPECIALIDADE"] = pd.to_numeric(
        dados_nominais["QUANTIDADE POR ESPECIALIDADE"],
        errors="coerce",
    )
    quantidade_por_vinculo = (
        dados_nominais.dropna(
            subset=["TIPO DE VÍNCULO", "QUANTIDADE POR ESPECIALIDADE"]
        )
        .groupby("TIPO DE VÍNCULO", as_index=False)[
            "QUANTIDADE POR ESPECIALIDADE"
        ]
        .sum()
    )
    grafico_vinculo = px.pie(
        quantidade_por_vinculo,
        names="TIPO DE VÍNCULO",
        values="QUANTIDADE POR ESPECIALIDADE",
        title="Profissionais por tipo de vínculo",
    )
    profissionais_por_vinculo = (
        dados_nominais.dropna(subset=["NOME", "TIPO DE VÍNCULO"])[
            ["NOME", "TIPO DE VÍNCULO"]
        ]
        .rename(
            columns={
                "NOME": "Nome",
                "TIPO DE VÍNCULO": "Tipo de vínculo",
            }
        )
    )
    col1, col2 = st.columns(2, border=True)
    col1.plotly_chart(grafico_vinculo, width="stretch")
    col2.dataframe(
        profissionais_por_vinculo,
        hide_index=True,
        width="stretch",
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
            title="Dados de Profissionais",
            icon="📊",
            default=True,
        ),
        exames_page,
    ]
)

navigation.run()