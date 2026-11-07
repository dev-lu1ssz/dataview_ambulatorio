import base64
import mimetypes
from pathlib import Path

import streamlit as st
from streamlit_card import card

st.set_page_config(page_title="Painel de dados")

st.title('Hospital Universitário Pedro Ernesto')
st.image('imagens/pedro_ernesto.jpeg', caption='Imagem da área externa') # Adicionar imagem
st.text('O Hospital Universitário Pedro Ernesto (HUPE) é o hospital universitário da Universidade do Estado do Rio de Janeiro (UERJ). Foi inaugurado no ano de 1950, sendo parte da rede hospitalar da Secretaria de Saúde do então Distrito Federal. Em 1962 passou a integrar a Universidade do Estado da Guanabara (UEG), que mais tarde se tornaria a UERJ.')
st.markdown('## Sobre o painel')
st.text('Este é um painel que tem como objetivo apresentar diferentes tipos de gráficos para facilitar a visualização dos dados de desempenho do ambulatório nos anos de 2021 a 2024. Todas as informações apresentadas são utilizando a base de dados disponibilizada pelo Yago Moraes Costa.')
st.text('Selecione um dos cards abaixo e veja os dados do ambulatório:')
st.subheader('Acesse os dados')

cards = [
    {
        "titulo": "Profissionais",
        "descricao": "Dados de profissionais e sua distribuição no ambulatório",
        "pagina": "pages/profissionais.py",
        "imagem": "imagens/cirurgia.jpg",
    },
    {
        "titulo": "Relatórios - 2021",
        "descricao": "Relatórios de atendimentos, exames e procedimentos",
        "pagina": "pages/relatorio_2021.py",
        "imagem": "imagens/dados.jpg",
    },
    {
        "titulo": "Relatórios - 2022",
        "descricao": "Relatórios de atendimentos e exames",
        "pagina": "pages/relatorio_2022.py",
        "imagem": "imagens/dados2.jpg",
    },
    {
        "titulo": "Relatórios - 2023",
        "descricao": "Relatórios de atendimentos, exames e procedimentos",
        "pagina": "pages/relatorio_2023.py",
        "imagem": "imagens/dados3.jpg",
    },
    {
        "titulo": "Relatórios - 2024",
        "descricao": "Relatórios de atendimentos, exames e procedimentos",
        "pagina": "pages/relatorio_2024.py",
        "imagem": "imagens/dados4.jpg",
    },
]
card_styles = {
    "card": {
        "width": "350px",
        "height": "500px",
        "border-radius": "12px",
        "box-shadow": "0 4px 12px rgba(0, 0, 0, 0.12)",
    },
    "text": {
        "font-size": "16px"    

    },
}


def imagem_para_card(caminho):
    if not caminho or caminho.startswith(("http://", "https://", "data:")):
        return caminho

    arquivo = Path(caminho).expanduser()
    if not arquivo.is_absolute():
        arquivo = Path(__file__).resolve().parent / arquivo
    if not arquivo.is_file():
        raise FileNotFoundError(f"Imagem do card não encontrada: {arquivo}")

    tipo_mime, _ = mimetypes.guess_type(arquivo.name)
    if not tipo_mime or not tipo_mime.startswith("image/"):
        raise ValueError(f"O arquivo não parece ser uma imagem: {arquivo}")

    imagem_codificada = base64.b64encode(arquivo.read_bytes()).decode("ascii")
    return f"data:{tipo_mime};base64,{imagem_codificada}"


def mostrar_card(dados_card):
    selecionado = card(
        title=dados_card["titulo"],
        text=dados_card["descricao"],
        image=imagem_para_card(dados_card["imagem"]),
        url=None,
        styles=card_styles,
        key=f"card-{dados_card['pagina']}",
    )
    if selecionado:
        st.switch_page(dados_card["pagina"])


for dados_card in cards:
    mostrar_card(dados_card)