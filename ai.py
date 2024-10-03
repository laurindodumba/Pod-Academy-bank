import streamlit as st

# ai.py
import streamlit as st

def save_api_settings(api_key, default_user, model_option):
    # Aqui você implementa a lógica para salvar as configurações
    # Por exemplo, salvar em um arquivo, variáveis de ambiente, etc.
    pass

def config_page():
    st.title("CONFIGURAÇÃO")
    st.write("Parâmetros de configuração da API")

    with st.form("api_config"):
        api_key = st.text_input("Chave da API", type="password", help="Insira sua chave da API da OpenAI.")
        default_user = st.text_input("Usuário Padrão", help="Insira o identificador do usuário padrão.")
        model_option = st.selectbox("Modelo Padrão", ['gpt-3.5-turbo', 'text-embedding-ada-002', 'text-davinci-003'], help="Selecione o modelo de IA padrão para operações.")
        
        submit_button = st.form_submit_button("Salvar Configurações")
        
        if submit_button:
            save_api_settings(api_key, default_user, model_option)
            st.success("Configurações salvas com sucesso!")
