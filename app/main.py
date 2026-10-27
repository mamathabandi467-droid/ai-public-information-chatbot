
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.semantic_search import search_information
from app.intent_classifier import classify_intent
from app.llm_service import generate_answer

app = FastAPI(title="AI Public Information Chatbot")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/health")
async def health():
    return {"status": "running"}


@app.post("/chat")
async def chat(data: ChatRequest):
    message = data.message.strip()

    if not message:
        return {"reply": "Please enter your question."}

    intent = classify_intent(message)
    results = search_information(message)

    if not results:
        return {
            "reply": (
                "Sorry, I couldn't find matching information "
                "in the database."
            )
        }

    item = results[0]

    context = (
        f"Organization: {item.get('organization_name', '')}\n"
        f"Category: {item.get('category', '')}\n"
        f"Location: {item.get('location', '')}\n"
        f"Contact: {item.get('contact', '')}\n"
        f"Services: {item.get('services', '')}\n"
        f"Operating hours: {item.get('operating_hours', '')}\n"
        f"FAQ: {item.get('faq', '')}\n"
        f"Answer: {item.get('answer', '')}"
    )

    answer = generate_answer(message, context)

    reply = (
        f"{answer}\n\n"
        f"Detected intent: {intent}\n"
        f"Organization: {item.get('organization_name', '')}\n"
        f"Source: {item.get('source_url', '')}"
    )

    return {
        "reply": reply,
        "intent": intent,
        "organization": item.get("organization_name", ""),
        "source": item.get("source_url", "")
    }
