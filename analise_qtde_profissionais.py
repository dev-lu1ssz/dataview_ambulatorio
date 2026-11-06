from pathlib import Path
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Painel de dados")
st.title("Quantidade de profissionais por especialidade")

arquivo_dados = Path(__file__).with_name("qtde_profissionais.xlsx")
dados = pd.read_excel(arquivo_dados).dropna()
dados = dados.rename(
    columns={
        "PROFISSIONAIS ENVOLVIDOS NA ASSISTÊNCIA DO AMBULATÓRIO PÓS COVID": "Especialidade",
        "Unnamed: 1": "2021",
        "Unnamed: 2": "2022",
        "Unnamed: 3": "2023",
        "Unnamed: 4": "2024",
    }
)

anos = ["2021", "2022", "2023", "2024"]
dados[anos] = dados[anos].apply(pd.to_numeric).astype("int64")

especialidade_selecionada = st.selectbox(
    "Selecione a especialidade que deseja visualizar",
    options=dados["Especialidade"].tolist(),
)

quantidades = dados.loc[
    dados["Especialidade"] == especialidade_selecionada, anos
].iloc[0]
grafico = pd.DataFrame(
    {"Ano": anos, "Quantidade": quantidades.to_numpy()}
)

st.subheader(especialidade_selecionada)
st.line_chart(grafico, x="Ano", y="Quantidade", color='green')
