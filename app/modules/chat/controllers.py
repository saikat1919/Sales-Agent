from fastapi import APIRouter
from app.integrations.llm.base import ChatMessage
from app.integrations.llm.dependencies import LLMDep

router = APIRouter(prefix="/chat", tags=["chat"])

router.get("/basic")
async def basic_call(llm: LLMDep) -> dict[str, str]:
    messages = [
        ChatMessage(
            role="user",
            content="Say Hello to Kinbo's customers in one sentence."
        )
    ]
    reply = await llm.chat(system="", messages=messages)
    return {"reply": reply}