from fastapi import FastAPI

from app.api.routes import router

from app.logging_config import setup_logging

setup_logging()
app = FastAPI(
    title="Simple LLM Chatbot",
    version="0.3.0",
    description="Search-based chatbot",
)

app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
