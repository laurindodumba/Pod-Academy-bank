import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns



# Função para injetar Bootstrap
def inject_bootstrap():
    bootstrap_link = """
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    """
    st.markdown(bootstrap_link, unsafe_allow_html=True)

# Função para criar o rodapé
def create_footer():
    footer_html = """
        <div class="footer">
        <hr style="border-top: 1px solid #bbb;">
        <p style="text-align: center; font-size: 14px;">© 2024 PoD Bank - Laurindo</p>
        </div>
        """
    st.markdown(footer_html, unsafe_allow_html=True)

# Função para converter imagem em base64
def get_image_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Função para upload de arquivo e análise
def upload_file():
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Arquivo carregado com sucesso!")
        st.write(df)

        # Análise de crédito
        analise_total = df["AMT_INCOME_TOTAL"].sum()
        moda_credito = df["AMT_CREDIT"].mode()[0]  # Acessa o primeiro valor da moda
        mean_credito = df["AMT_CREDIT"].mean()
        med_credito = df["AMT_CREDIT"].median()

        # Divisão em colunas
        total1, total2, total3, total4 = st.columns(4, gap='large')

        with total1:
            st.info("SOMA", icon="💸")
            st.metric(label="SOMA", value=f"{analise_total:,.0f}")

        with total2:
            st.info("MODA", icon="💼")
            st.metric(label="MODA", value=f"{moda_credito:,.0f}")

        with total3:
            st.info("MÉDIA", icon="💼")
            st.metric(label="MÉDIA", value=f"{mean_credito:,.0f}")

        with total4:
            st.info("MEDIANA", icon="📅")
            st.metric(label="MEDIANA", value=f"{med_credito:,.0f}")

        # Histograma da Renda Total
        fig, ax = plt.subplots(figsize=(8, 5))
        df['AMT_CREDIT'].hist(bins=30, color='skyblue', edgecolor='black', ax=ax)
        ax.set_title('Distribuição de Crédito')
        ax.set_xlabel('Renda Total')
        ax.set_ylabel('Frequência')
        st.pyplot(fig)

        # Gráfico de Distribuição do Crédito
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df['AMT_CREDIT'], kde=True, color="blue", ax=ax)
        ax.set_title('Distribuição do Crédito')
        ax.set_xlabel('Crédito')
        ax.set_ylabel('Densidade')
        st.pyplot(fig)

        # Gráfico de dispersão entre Renda e Crédito
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(x='AMT_INCOME_TOTAL', y='AMT_CREDIT', data=df, ax=ax, color='purple')
        ax.set_title('Relação entre Renda e Crédito', fontsize=16)
        ax.set_xlabel('Renda Total', fontsize=12)
        ax.set_ylabel('Crédito', fontsize=12)
        st.pyplot(fig)

        # Gráfico de Barras das Categorias de Emprego
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(x='OCCUPATION_TYPE', data=df, palette='viridis', ax=ax)
        ax.set_title('Distribuição das Categorias de Emprego', fontsize=16)
        ax.set_xlabel('Tipo de Ocupação', fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.set_ylabel('Contagem', fontsize=12)
        st.pyplot(fig)
        
        return df
    else:
        st.write("Nenhum arquivo foi enviado ainda.")
        return None

# Configurações da página
st.set_page_config(page_title="POD BANK - APPLICATION", layout="wide")

# Injeta Bootstrap CSS
inject_bootstrap()

# Seleção de páginas
page = st.sidebar.selectbox("Navegação", ["HOME", "SERVIÇOS", "INSIGHTS", "SOBRE NÓS"])

# Lógica de navegação entre as páginas
if page == "HOME":
    st.markdown("<h1 style='text-align: center;'>APLICAÇÃO WEB - POD BANK</h1>", unsafe_allow_html=True)
    
    # Caminho da imagem
    # image_path = r"C:\Users\Eduardo\Documents\Pod Academy\pod bank\Capturar.PNG"
    # image_base64 = get_image_base64(image_path)
    
    # HTML/CSS para exibir a imagem com bordas arredondadas
    # image_html = f"""
    # <style>
    # img {{
    #     border-radius: 15px;  /* Arredonda as bordas da imagem */
    # }}
    # </style>
    # <img src="data:image/png;base64,{image_base64}" width="1000">
    # """
    
    # st.markdown(image_html, unsafe_allow_html=True)

elif page == "SERVIÇOS":
    st.title("SERVIÇOS")
    create_footer()

elif page == "INSIGHTS":
    st.title("ANÁLISE ESTATÍSTICA")
    df = upload_file()  # Função de upload e análise de dados
    create_footer()

elif page == "SOBRE NÓS":
    st.title("SOBRE NÓS")
    st.write("Informações sobre a PoD Bank.")
    create_footer()
