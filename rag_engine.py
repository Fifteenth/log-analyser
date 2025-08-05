from dotenv import load_dotenv


from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")



def create_vector_store(chunks):
    docs = [Document(page_content=chunk) for chunk in chunks]
    vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())
    return vector_store

def answer_query(vector_store, query):
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4", temperature=0),
        retriever=vector_store.as_retriever()
    )
    return qa.run(query)
