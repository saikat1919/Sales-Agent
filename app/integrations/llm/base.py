from typing import Literal, Protocol, Any
from pydantic import BaseModel
from collections.abc import Awaitable, Callable

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ToolSpec(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]

ToolRunner = Callable[[str, dict[str, Any]], Awaitable[dict[str, Any]]]

class LLMReply(BaseModel):
    text: str
    tool_calls: list[str] = []

class LLMProvider(Protocol):
    async def chat(self, system: str, message: list[ChatMessage]) -> str:
        ...

    async def chat_with_tool(
            self,
            system: str,
            messages: list[ChatMessage],
            tools: list[ToolSpec],
            run_tool: ToolRunner,
    ) -> LLMReply: ...