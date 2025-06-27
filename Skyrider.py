import streamlit as st
import pandas as pd
import time

def main():
    st.title("App de Visualização de Datasets")
    if "df" not in st.session_state:
        st.session_state.df = None


    if "df_agrupado" not in st.session_state:
        st.session_state.df_agrupado = None


    if "vendas_dict" not in st.session_state:
        st.session_state.vendas_dict = None


    if "colunas_agrupamento" not in st.session_state:
        st.session_state.colunas_agrupamento = None


    # Menu lateral
    opcao = st.sidebar.selectbox(
        "SELECIONE A FUNÇÃO:",
        options=["Carregar dataset", 
                "Visualizar dataset", 
                "Agrupar dados",
                "Buscar quantidade (DataFrame)",
                "Buscar quantidade (Dict)"]
    )


    if opcao == "Carregar dataset":
        # Upload do CSV
        arquivo = st.sidebar.file_uploader("Upload do arquivo CSV", type=["csv"])
        if arquivo is not None:
            # Leitura do DataFrame
            df = pd.read_csv(arquivo, parse_dates=["purchase_date"])
            st.session_state.df = df
            st.session_state.df_agrupado = None
            st.session_state.vendas_dict = None
            st.session_state.colunas_agrupamento = None
            st.success("Dataset carregado com sucesso!")

    if opcao == "Visualizar dataset":
        if st.session_state.df is not None:
            st.dataframe(st.session_state.df, height=300)

    if opcao == "Agrupar dados":
        if st.session_state.df is not None:
            df = st.session_state.df
            st.subheader("Agrupamento de dados por df")
            cols = df.columns.tolist()
            col1 = st.sidebar.selectbox("Atributo 1:", cols, index=1)
            col2 = st.sidebar.selectbox("Atributo 2:", cols, index=2)
            col3 = st.sidebar.selectbox("Atributo somador:", cols, index=4)



if __name__ == '__main__':
    main()
