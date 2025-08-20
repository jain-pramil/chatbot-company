from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routers import chatbot
import os
import json

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chatbot.router, prefix="/chatbot")

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Debug print
print(app.routes)

# Routes
@app.get("/", response_class=HTMLResponse)
async def faq_form(request: Request):
    return templates.TemplateResponse("faq_form.html", {"request": request})


@app.get("/faqs", response_class=HTMLResponse)
async def view_faqs(request: Request, company_id: str):
    metadata_path = f"data/{company_id}/faiss_index/metadata.json"
    faqs = []

    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            faqs = [item["text"] for item in metadata]

    return templates.TemplateResponse("faq_list.html", {
        "request": request,
        "company_id": company_id,
        "faqs": faqs
    })


@app.get("/chat-widget/{company_id}", response_class=HTMLResponse)
async def chat_widget(request: Request, company_id: str):
    return templates.TemplateResponse(
        "chat-widget.html",
        {"request": request, "company_id": company_id}
    )
