import os
from typing import Any, Dict, Optional
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables (prefer setting GEMINI_API_KEY in the terminal)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize LLM only if API key is present
llm: Optional[ChatGoogleGenerativeAI] = None
if GEMINI_API_KEY:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY
    )

# Initialize session state for the chat
st.session_state.setdefault("messages", [])
st.session_state.setdefault("dataset_info", None)


def analyze_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """Return a summary dictionary for the given DataFrame."""
    summary: Dict[str, Any] = {}
    summary["shape"] = df.shape
    summary["columns"] = list(df.columns)
    summary["dtypes"] = df.dtypes.astype(str).to_dict()
    summary["null_values"] = df.isnull().sum().to_dict()
    summary["statistics"] = df.describe().to_dict()
    return summary


def answer_question(question: str, dataset_info: Dict[str, Any], df_sample: str) -> str:
    """
    Build a prompt and ask the LLM to answer a user question about the dataset.
    Returns the assistant text or an error message if the model is unavailable.
    """
    prompt = (
        "You are a data-analysis assistant.\n"
        f'The user uploaded a dataset and asked: "{question}"\n\n'
        "Dataset information:\n"
        f"{dataset_info}\n\n"
        "Sample of the data (first 5 rows):\n"
        f"{df_sample}\n\n"
        "Answer clearly and concisely in English. If specific analysis is needed, "
        "suggest relevant steps and insights based on the available data." \
        "You must not make up any data."
    )

    if llm is None:
        return (
            "Model not initialized. Please set the GEMINI_API_KEY environment variable "
            "in your terminal (or in a .env) and restart the app."
        )

    response = llm.invoke(prompt)
    return response.content if hasattr(response, "content") else str(response)


# Streamlit UI
st.title("📊 Data Analyst Assistant with AI")

col1, _col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Data preview")
        st.write(df.head())

        summary = analyze_dataset(df)
        st.session_state.dataset_info = summary

        st.subheader("Statistical summary")
        st.json(summary)

with st.sidebar:
    st.header("🤖 AI Assistant")
    st.write("Ask questions about your uploaded data.")

    if st.session_state.dataset_info is not None:
        if llm is None:
            st.warning(
                "GEMINI_API_KEY not set. Set the environment variable in the terminal "
                "before running Streamlit to enable the AI assistant."
            )

        chat_container = st.container()

        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        if prompt := st.chat_input("Type your question about the data..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.spinner("Thinking..."):
                df_sample = df.head().to_string() if "df" in locals() else "Data not available"
                reply = answer_question(prompt, st.session_state.dataset_info, df_sample)

            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    else:
        st.info("📁 Upload a CSV file to start asking questions about your data!")

# Small CSS tweaks
st.markdown(
    """
<style>
    .stChatMessage { margin-bottom: 1rem; }
    .sidebar .stContainer { padding-top: 1rem; }
</style>
""",
    unsafe_allow_html=True,
)
