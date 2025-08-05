import streamlit as st
from log_utils import split_logs
from rag_engine import create_vector_store, answer_query

st.title("🔍 Log Analysis Assistant (OpenAI + Streamlit)")

uploaded_file = st.file_uploader("Upload a .log or .txt file", type=["log", "txt"])
if uploaded_file:
    log_text = uploaded_file.read().decode("utf-8")
    chunks = split_logs(log_text)
    db = create_vector_store(chunks)

    question = st.text_input("Ask a question about the logs")
    if question:
        answer = answer_query(db, question)
        st.write("### 💡 Answer")
        st.write(answer)


# import sys
# import streamlit as st

# st.write("Python executable used:", sys.executable)
# st.write("Python version:", sys.version)
