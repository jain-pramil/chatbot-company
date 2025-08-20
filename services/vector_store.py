import os
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from services.embedder import embedding_model

def create_or_load_faiss_index(text: str, company_id: str):
    index_dir = f"data/{company_id}/faiss_index"
    os.makedirs(index_dir, exist_ok=True)

    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=chunk) for chunk in splitter.split_text(text)]

    # Load existing vectorstore or create a new one
    if os.path.exists(os.path.join(index_dir, "index.faiss")):
        vectorstore = FAISS.load_local(index_dir, embedding_model, allow_dangerous_deserialization=True)
        vectorstore.add_documents(docs)
    else:
        vectorstore = FAISS.from_documents(docs, embedding_model)

    # Save vectorstore
    vectorstore.save_local(index_dir)

def load_vector_store(company_id: str):
    index_dir = f"data/{company_id}/faiss_index"
    if os.path.exists(os.path.join(index_dir, "index.faiss")):
        return FAISS.load_local(index_dir, embedding_model, allow_dangerous_deserialization=True)
    else:
        return None

# (Optional) Use this version if you want to store vector DB separately under /vectorstore/
def save_vector_store(vectorstore, company_id: str):
    save_path = os.path.join("vectorstore", company_id)
    os.makedirs(save_path, exist_ok=True)
    vectorstore.save_local(save_path)

def load_vector_store_from_vectorstore(company_id: str, embedding_model):
    index_dir = os.path.join("vectorstore", company_id)
    return FAISS.load_local(index_dir, embedding_model, allow_dangerous_deserialization=True)
