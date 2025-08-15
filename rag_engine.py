from dotenv import load_dotenv


from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

import os
import streamlit as st
#import openai
from openai import OpenAI

load_dotenv()


# 1openai_api_key = os.getenv("OPENAI_API_KEY")

openai_api_key = st.secrets["OPENAI_API_KEY"]


def create_vector_store(chunks):
    docs = [Document(page_content=chunk) for chunk in chunks]
    vector_store = FAISS.from_documents(
        docs, 
        OpenAIEmbeddings())
    return vector_store


# def answer_query(vector_store, query):
#     qa = RetrievalQA.from_chain_type(
#         llm=ChatOpenAI(model="gpt-4", temperature=0),
#         retriever=vector_store.as_retriever()
#     )
#     return qa.run(query)



client = OpenAI()
def answer_query(db, question, system_prompt=None, top_k=5):
    docs = db.similarity_search(question, k=top_k)
    if not docs:
        return "Information not found in the logs."

    retrieved_logs = "\n\n".join([doc.page_content for doc in docs])

    user_prompt = f"""
Here are the relevant log excerpts:

{retrieved_logs}

User question: {question}

Answer ONLY based on the logs above, citing line numbers and timestamps where applicable.
"""

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0,
    )

    return response.choices[0].message.content.strip()
