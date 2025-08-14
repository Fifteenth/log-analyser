#import time 
import streamlit as st
from log_utils import split_logs
from rag_engine import create_vector_store, answer_query

SYSTEM_PROMPT = """
You are a Log Analysis Assistant. Your role is to read and analyse log files provided by the user.

Rules:
1. Always base answers on the provided log data.
2. Cite the log lines or time ranges that support your answer.
3. If unsure, say 'Information not found in the logs.'
4. Provide clear, concise answers.
"""

# NEW: Sanitisation function to prevent prompt injection
def sanitize_user_input(user_input: str) -> str:
    blocked_patterns = ["ignore previous", "disregard instructions", "system prompt", "override rules"]
    lowered = user_input.lower()
    if any(p in lowered for p in blocked_patterns):
        return "[Potential prompt injection detected — input blocked]"
    return user_input

def check_password():
    """Returns `True` if the user entered the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Remove password from session
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Log Analysis", "About Us", "Methodology"])


# Initialise session state for history
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

def ask_question():
    # question = st.session_state.question_input
    raw_question = st.session_state.question_input
    question = sanitize_user_input(raw_question)  # 🔹 NEW: sanitise before sending
    if question:
        answer = answer_query(db, question, system_prompt=SYSTEM_PROMPT)
        st.session_state.qa_history.append({"question": question, "answer": answer})
        st.session_state.question_input = ""


if page == "Log Analysis":
    st.title("🔍 Log Analysis Assistant (OpenAI + Streamlit)")

    uploaded_file = st.file_uploader("Upload a .log or .txt file", type=["log", "txt"])

    if uploaded_file:
        log_text = uploaded_file.read().decode("utf-8")
        chunks = split_logs(log_text)
        db = create_vector_store(chunks)

        # st.text_input("Ask a question about the logs:", key="question_input", on_change=ask_question)

        # Display history
        if st.session_state.qa_history:
            st.write("## 📜 Question & Answer History")
            for i, entry in enumerate(st.session_state.qa_history, 1):
                st.markdown(f"**Q{i}:** {entry['question']}")
                st.markdown(f"**A{i}:** {entry['answer']}")
                st.markdown("---")


        # HTML anchor for scrolling
            st.markdown("<div id='end'></div>", unsafe_allow_html=True)

            # JavaScript to scroll to anchor
            st.markdown(
                "<script>document.getElementById('end').scrollIntoView({behavior: 'smooth'});</script>",
                unsafe_allow_html=True
            )

        st.text_input("Ask a question about the logs:", key="question_input", on_change=ask_question)


elif page == "About Us":
    st.title("ℹ️ About Us")
    st.write("""
    This app is built to help users quickly analyse log files using RAG (Retrieval-Augmented Generation) technology.
    It combines OpenAI’s LLM with semantic search to answer your log-related questions.
    """)

elif page == "Methodology":
    st.title("📚 Methodology")
    st.write("""
    1. **Chunking Logs** – The uploaded log file is split into smaller, manageable text chunks.
    2. **Vector Store Creation** – Chunks are embedded into numerical vectors and stored in a vector database.
    3. **Query Matching** – When a user asks a question, the most relevant chunks are retrieved.
    4. **LLM Answer Generation** – OpenAI’s model generates a concise answer using the retrieved log context.
    """)

