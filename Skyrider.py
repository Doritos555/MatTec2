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

if __name__ == '__main__':
    main()
