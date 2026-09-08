from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Simple LLM Chatbot",
    version="0.3.0",
    description="Search-based chatbot",
)

app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
