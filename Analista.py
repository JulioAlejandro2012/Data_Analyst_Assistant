import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inicializa LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)

# Inicializa session state para o chat
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dataset_info" not in st.session_state:
    st.session_state.dataset_info = None

# Função para análise
def analisar_dataset(df):
    resumo = {}
    resumo["Linhas e Colunas"] = df.shape
    resumo["Colunas"] = list(df.columns)
    resumo["Tipos de Dados"] = df.dtypes.astype(str).to_dict()
    resumo["Valores Nulos"] = df.isnull().sum().to_dict()
    resumo["Estatísticas"] = df.describe().to_dict()

    return resumo

# Função para responder perguntas sobre o dataset
def responder_pergunta(pergunta, dataset_info, df_sample):
    prompt = f"""
    Você é um assistente especializado em análise de dados.
    O usuário carregou um dataset e fez a seguinte pergunta: "{pergunta}"

    Informações sobre o dataset:
    {dataset_info}

    Amostra dos dados (primeiras 5 linhas):
    {df_sample}

    Responda de forma clara, objetiva e útil em português. Se a pergunta for sobre análises específicas, 
    sugira insights relevantes baseados nos dados disponíveis.
    """
    response = llm.invoke(prompt)
    return response.content if hasattr(response, 'content') else str(response)

# Interface principal
st.title("📊 Analista de Dados com IA Assistente")

# Layout com colunas
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Envie seu arquivo CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Prévia dos Dados")
        st.write(df.head())

        resumo = analisar_dataset(df)
        
        # Armazena informações do dataset no session state
        st.session_state.dataset_info = resumo
        
        st.subheader("Resumo Estatístico")
        st.json(resumo)

# Chatbot na sidebar
with st.sidebar:
    st.header("🤖 Assistente IA")
    st.write("Faça perguntas sobre seus dados!")
    
    if st.session_state.dataset_info is not None:
        # Container para as mensagens do chat
        chat_container = st.container()
        
        # Exibe mensagens do chat
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
        
        # Input para nova pergunta
        if prompt := st.chat_input("Digite sua pergunta sobre os dados..."):
            # Adiciona pergunta do usuário
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Gera resposta da IA
            with st.spinner("Pensando..."):
                df_sample = df.head().to_string() if 'df' in locals() else "Dados não disponíveis"
                resposta = responder_pergunta(prompt, st.session_state.dataset_info, df_sample)
            
            # Adiciona resposta da IA
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            
            # Rerun para atualizar o chat
            st.rerun()
        
        # Botão para limpar chat
        if st.button("🗑️ Limpar Chat"):
            st.session_state.messages = []
            st.rerun()
    
    else:
        st.info("📁 Carregue um arquivo CSV para começar a conversar sobre seus dados!")

# CSS para melhorar a aparência
st.markdown("""
<style>
    .stChatMessage {
        margin-bottom: 1rem;
    }
    .sidebar .stContainer {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)
