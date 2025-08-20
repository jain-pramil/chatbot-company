from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS

from services.embedder import embedding_model
from services.vector_store import create_or_load_faiss_index
from utils.file_loader import extract_text_from_file, extract_text_from_url

import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Data model
class FAQItem(BaseModel):
    question: str
    answer: str
    company_id: str


# Routes
@router.post("/upload/")
async def upload_file_or_url(
    company_id: str = Form(...),
    file: UploadFile = File(None),
    url: str = Form(None)
):
    """
    Accepts a file or a URL to upload data, extract text, and index it for a given company.
    """
    try:
        text = None
        upload_dir = os.path.join("data", company_id, "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        # File upload
        if file and file.filename:
            file_path = os.path.join(upload_dir, file.filename)
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            text = extract_text_from_file(file_path)

        # URL upload
        elif url:
            with open(os.path.join(upload_dir, "urls.txt"), "a") as f:
                f.write(url + "\n")
            text = extract_text_from_url(url)

        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Either file or URL must be provided."}
            )

        if not text or not text.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Failed to extract text."}
            )

        # Index content
        create_or_load_faiss_index(text, company_id)
        return {"message": "Content uploaded and indexed successfully."}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.post("/ask/{company_id}")
async def ask_question(company_id: str, question: str = Form(...)):
    try:
        index_dir = f"data/{company_id}/faiss_index"
        if not os.path.exists(index_dir):
            return JSONResponse(
                status_code=404,
                content={"error": "No data found for this company."}
            )

        vectorstore = FAISS.load_local(
            index_dir,
            embedding_model,
            allow_dangerous_deserialization=True
        )
        retriever = vectorstore.as_retriever()
        docs = retriever.get_relevant_documents(question)

        print("Retrieved Chunks:")
        for d in docs:
            print(d.page_content)

        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-3.5-turbo"),
            retriever=retriever
        )

        result = qa.run(question)
        return {"answer": result}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.post("/add-faq/")
async def add_faq(
    company_id: str = Form(...),
    question: str = Form(...),
    answer: str = Form(...)
):
    content = f"Q: {question}\nA: {answer}"
    create_or_load_faiss_index(text=content, company_id=company_id)
    return {"message": "FAQ added to knowledge base"}


@router.get("/chat/{company_id}", response_class=HTMLResponse)
async def chat_page(request: Request, company_id: str):
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "company_id": company_id}
    )
