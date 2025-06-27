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
            df = pd.read_csv(arquivo, parse_dates=["purchase_date"])
            st.session_state.df = df
            st.session_state.df_agrupado = None
            st.session_state.vendas_dict = None
            st.session_state.colunas_agrupamento = None
            st.success("Dataset carregado com sucesso!")

    elif opcao == "Visualizar dataset":
        if st.session_state.df is not None:
            st.dataframe(st.session_state.df, height=300)
        else:
            st.warning("Nenhum dataset carregado!")

    elif opcao == "Agrupar dados":
        if st.session_state.df is not None:
            df = st.session_state.df
            st.subheader("Agrupamento de dados")
            cols = df.columns.tolist()
            col1 = st.sidebar.selectbox("Atributo 1:", cols, index=1)
            col2 = st.sidebar.selectbox("Atributo 2:", cols, index=2)
            col3 = st.sidebar.selectbox("Atributo somador:", cols, index=4)

            if st.sidebar.button("Executar agrupamento"):
                df_agrupado = df.groupby([col1, col2])[col3].sum().reset_index()
                st.session_state.df_agrupado = df_agrupado
                st.session_state.colunas_agrupamento = (col1, col2)
                st.session_state.vendas_dict = df_agrupado.set_index([col1, col2])[col3].to_dict()
                st.success("Dados agrupados com sucesso!")

            if st.session_state.df_agrupado is not None:
                st.dataframe(st.session_state.df_agrupado)

        else:
            st.warning("Nenhum dataset carregado!")

    elif opcao == "Buscar quantidade (DataFrame)":
        if st.session_state.df_agrupado is not None:
            col1, col2 = st.session_state.colunas_agrupamento
            val1 = st.sidebar.text_input(f"Valor para {col1}:")
            val2 = st.sidebar.text_input(f"Valor para {col2}:")

            if st.sidebar.button("Buscar"):
                df_filtro = st.session_state.df_agrupado
                resultado = df_filtro[(df_filtro[col1] == val1) & (df_filtro[col2] == val2)]
                if not resultado.empty:
                    st.write(f"Quantidade encontrada: {resultado.iloc[0, 2]}")
                else:
                    st.write("Nenhum resultado encontrado.")
        else:
            st.warning("Nenhum agrupamento realizado ainda!")

    elif opcao == "Buscar quantidade (Dict)":
        if st.session_state.vendas_dict is not None:
            col1, col2 = st.session_state.colunas_agrupamento
            val1 = st.sidebar.text_input(f"Valor para {col1}:")
            val2 = st.sidebar.text_input(f"Valor para {col2}:")

            if st.sidebar.button("Buscar no Dict"):
                chave = (val1, val2)
                if chave in st.session_state.vendas_dict:
                    st.write(f"Quantidade encontrada: {st.session_state.vendas_dict[chave]}")
                else:
                    st.write("Nenhum resultado encontrado.")
        else:
            st.warning("Nenhum agrupamento realizado ainda!")

if __name__ == '__main__':
    main()
