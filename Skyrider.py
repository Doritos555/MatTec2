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
            grouped = (df.groupby([col1, col2])[col3]
                        .sum()
                        .reset_index()
            )
            vendas_dict = grouped.set_index([col1, col2])[col3].to_dict()
            st.session_state.df_agrupado = grouped
            st.session_state.vendas_dict = vendas_dict
            st.session_state.colunas_agrupamento = (col1, col2, col3)
            st.dataframe(grouped, height=300)
            st.subheader("Agrupamento de dados por dict (10 primeiros)")
            #st.write(vendas_dict)
            dict_str = {str(k): v for k, v in list(vendas_dict.items())[:10]}
            st.write(dict_str)

    if opcao == "Buscar quantidade (DataFrame)":
        if st.session_state.df_agrupado is not None:
            col1, col2, col3 = st.session_state.colunas_agrupamento
            valor1 = st.sidebar.selectbox(f"Valor de {col1}:", 
                                        options=st.session_state.df_agrupado[col1].unique())
            valor2 = st.sidebar.selectbox(f"Valor de {col2}:", 
                                        options=st.session_state.df_agrupado[col2].unique())
            start = time.perf_counter()
            quantidade = st.session_state.df_agrupado[
                (st.session_state.df_agrupado[col1] == valor1) & 
                (st.session_state.df_agrupado[col2] == valor2)
            ][col3].values
            tempo = (time.perf_counter() - start) * 1000
            st.markdown(f"**Quantidade:** para {valor1} e {valor2} : {quantidade}")
            st.markdown(f"**Tempo:** {tempo:.4f} ms")




if __name__ == '__main__':
    main()
