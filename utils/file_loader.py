import os, requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import docx

def extract_text_from_file(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    else:
        raise ValueError("Unsupported file type")


def extract_text_from_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup.get_text(separator="\n")


# import requests
# from bs4 import BeautifulSoup
# import mimetypes
# import fitz  # PyMuPDF
# import tempfile

# def extract_text_from_url(url):
#     response = requests.get(url)
#     content_type = response.headers.get('Content-Type')

#     if "application/pdf" in content_type or url.lower().endswith(".pdf"):
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#             tmp_file.write(response.content)
#             tmp_file_path = tmp_file.name

#         doc = fitz.open(tmp_file_path)
#         text = ""
#         for page in doc:
#             text += page.get_text()
#         doc.close()
#         return text

#     elif "text/html" in content_type:
#         soup = BeautifulSoup(response.text, "html.parser")
#         return soup.get_text(separator="\n")

#     else:
#         return "Unsupported content type"
