import json
from fastapi import FastAPI
from models import ChatRequest, ChatResponse

app = FastAPI()

with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    latest_message = request.messages[-1].content.lower()
    conversation_text = " ".join(
    [msg.content.lower() for msg in request.messages]
)

    # Clarification logic
    vague_queries = [
        "assessment",
        "need assessment",
        "test",
        "need test"
    ]

    if latest_message in vague_queries:
        return {
            "reply": "Could you share the role, required skills, and seniority level?",
            "recommendations": [],
            "end_of_conversation": False
        }

    recommendations = []

    for item in catalog:

        name = item.get("name", "").lower()

        if any(word in name for word in conversation_text.split()):

            recommendations.append({
                "name": item["name"],
                "url": item["url"],
                "test_type": item.get("test_type", "K")
            })

    recommendations = recommendations[:10]

    return {
        "reply": "Here are recommended SHL assessments.",
        "recommendations": recommendations,
        "end_of_conversation": False
    }