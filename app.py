#import time 
import streamlit as st
from log_utils import split_logs
from rag_engine import create_vector_store, answer_query
from navigation import sidebar_navigation


SYSTEM_PROMPT = """
You are a Log Analysis Assistant. Your role is to read and analyse log files provided by the user.

Rules:
1. Always base answers on the provided log data.
2. Cite the log lines or time ranges that support your answer.
3. If unsure, say 'Information not found in the logs.'
4. Provide clear, concise answers.
"""

# Sanitisation function to prevent prompt injection
def sanitize_user_input(user_input: str) -> str:
    blocked_patterns = ["ignore previous", "disregard instructions", "system prompt", "override rules"]
    lowered = user_input.lower()
    if any(p in lowered for p in blocked_patterns):
        return "[Potential prompt injection detected — input blocked]"
    return user_input


def check_password():
    """Returns True if the user entered the correct password."""

    def password_entered():
        if st.session_state["password"] == st.secrets["PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    # ✅ If already logged in, skip rendering the login page
    if st.session_state.get("password_correct", False):
        return True

    # 🔹 Show login UI only when not logged in
    st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500&display=swap');

    /* Target Streamlit text input labels */
    label[data-testid="stWidgetLabel"] > div {
        font-family: 'Inter', sans-serif !important;
        font-size: 18px !important;
        font-weight: 500 !important;
        color: #222 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    
    with st.container():
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>🔒 Login</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Please enter your password to continue</p>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Password", type="password", on_change=password_entered, key="password")

            if "password_correct" in st.session_state and not st.session_state["password_correct"]:
                st.error("❌ Incorrect password. Please try again.")

    st.stop()  # ⛔ Prevent the rest of the app from rendering



def ask_question():
    # question = st.session_state.question_input
    raw_question = st.session_state.question_input
    question = sanitize_user_input(raw_question)  # 🔹 NEW: sanitise before sending
    if question:
        answer = answer_query(db, question, system_prompt=SYSTEM_PROMPT)
        st.session_state.qa_history.append({"question": question, "answer": answer})
        st.session_state.question_input = ""

if not check_password():
    st.stop()


# UI
st.set_page_config(page_title="Log Analysis Assistant", page_icon="🔍", layout="wide")


# Sidebar navigation
page = sidebar_navigation()



# Initialise session state for history
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []


if page == "Log Analysis":
    st.title("🔍 Log Analysis Assistant (OpenAI + Streamlit)")
    
    # Add disclaimer using expander
    with st.expander("⚠️ Disclaimer (click to expand)"):
        st.markdown("""

<span style="color:red;">IMPORTANT NOTICE:</span> This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

<span style="color:red;">Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.</span>

Always consult with qualified professionals for accurate and personalized advice.   

    """,
     unsafe_allow_html=True
     )

    uploaded_file = st.file_uploader("Upload a .log or .txt file", type=["log", "txt"])

    if uploaded_file:
        log_text = uploaded_file.read().decode("utf-8")
        chunks = split_logs(log_text)
        db = create_vector_store(chunks)

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


        st.markdown("### 💬 Ask a Question")
        st.text_input("Ask a question about the logs:", key="question_input", on_change=ask_question)




elif page == "About Us":
    st.title("ℹ️ About Us")

    st.markdown("""
    ## Project Scope
    The **Log Analysis Assistant** is designed to help engineers, analysts, and developers 
    quickly understand large and complex log files. By combining **semantic search** with 
    **large language models (LLMs)**, the tool reduces the time needed to diagnose issues, 
    trace errors, and extract meaningful insights from raw logs.

    ## Objectives
    - 🛠️ **Simplify Log Analysis** – Provide quick, natural language answers to log-related questions.  
    - 📈 **Improve Productivity** – Reduce time spent searching through lengthy log files manually.  
    - 🔒 **Ensure Safety** – Incorporate safeguards against prompt injection and unauthorised access.  
    - 🎯 **Accuracy** – Answers are grounded strictly in the provided log data.

    ## Data Sources
    - 📂 **User-Uploaded Logs** – Plain text (`.txt`) or log (`.log`) files.  
    - 🧩 **Chunking Strategy** – Logs are split into manageable segments with optional line numbers for better referencing.  
    - 📊 **Vector Store (FAISS)** – Chunks are embedded and stored for fast similarity search.  

    ## Features
    - 🔍 **Log File Upload** – Drag and drop `.log` or `.txt` files directly into the app.  
    - 💬 **Ask Questions in Natural Language** – Query logs just like chatting with a colleague.  
    - 🧠 **RAG (Retrieval-Augmented Generation)** – Ensures answers come only from uploaded logs.  
    - 📝 **Cited References** – Answers point back to specific log lines or timestamps.  
    - 📜 **History Tracking** – Keeps a Q&A history for review.  
    - 🔐 **Password Protection** – Optional login to restrict access.  
    - ⚡ **Lightweight UI** – Built with [Streamlit](https://streamlit.io) for simplicity and speed.  
    """)


elif page == "Methodology":
    # st.title("📚 Methodology")
    # st.success("""
    # 1. **Chunking Logs** – The uploaded log file is split into smaller, manageable text chunks.
    # 2. **Vector Store Creation** – Chunks are embedded into numerical vectors and stored in a vector database.
    # 3. **Query Matching** – When a user asks a question, the most relevant chunks are retrieved.
    # 4. **LLM Answer Generation** – OpenAI’s model generates a concise answer using the retrieved log context.
    # """)

    st.title("📑 Methodology")

    # -------------------------
    # Data Flow Overview
    # -------------------------
    st.header("1. Data Flow Overview")
    st.markdown("""
    The application processes uploaded log files and enables intelligent queries through Retrieval-Augmented Generation (RAG).

    **Overall Data Flow:**
    1. **File Upload** → User uploads `.log` or `.txt` file  
    2. **Pre-processing** → Logs are split into chunks with line numbers and timestamps  
    3. **Vectorisation** → Embeddings are created and stored in a vector database  
    4. **Query Input** → User asks a question in natural language  
    5. **Retrieval** → System searches for relevant log entries  
    6. **Response Generation** → Results are returned with supporting evidence (line numbers + timestamps)  
    """)

    # -------------------------
    # Use Case A
    # -------------------------
    st.header("2. Use Case A: Print Error Logs with Timing and Line Number")
    st.markdown("""
    **Process Flow:**
    - User asks for error logs  
    - Query parser detects `"error"`  
    - Relevant log chunks retrieved  
    - System extracts and presents error messages with timestamps and line numbers  
    """)

    st.graphviz_chart("""
    digraph {
        node [shape=box, style=rounded, color=black, fontname=Arial];
        "User Input ('Show error logs')" -> "Parse Query (detect 'error')" -> "Search Vector DB" -> "Return error logs (time + line no.)"
    }
    """)

    # -------------------------
    # Use Case B
    # -------------------------
    st.header("3. Use Case B: Check Login for Specified Users")
    st.markdown("""
    **Process Flow:**
    - User asks about login activity of a specific user  
    - Query parser extracts the username  
    - Relevant log chunks retrieved  
    - System filters for login events and presents results with timestamps and line numbers  
    """)

    st.graphviz_chart("""
    digraph {
        node [shape=box, style=rounded, color=black, fontname=Arial];
        "User Input ('Did Alice log in?')" -> "Parse Query (extract username)" -> "Search Vector DB" -> "Return login logs (time + line no.)"
    }
    """)

    # -------------------------
    # Implementation Details
    # -------------------------
    st.header("4. Implementation Details")
    st.markdown("""
    - **Frontend:** Streamlit for user interface  
    - **Core Functions:**  
        - `split_logs()` → splits log into chunks, adds line numbers & timestamps  
        - `create_vector_store()` → creates embeddings, stores in FAISS/Chroma  
        - `answer_query()` → interprets query, retrieves relevant logs, formats results  
    - **Safeguards:**  
        - Only answers based on provided logs  
        - Always cites supporting log lines  
        - Filters out irrelevant or malicious instructions  
    """)


