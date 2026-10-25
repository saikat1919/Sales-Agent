from google import genai
from google.genai import types, errors
from app.integrations.llm.base import ChatMessage
from app.core.exceptions.errors import LLMUnavailableError


ROLES = {
    "user": "user",
    "assistant": "assistant"
}

class GeminiProvider:
    def __init__(self, api_key: str, model: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def chat(self, system: str, messages: list[ChatMessage]) -> str:
        contents = [
            types.Content(role=ROLES[m.role], parts=[types.Part.from_text(text=m.content)])
            for m in messages
        ]

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(system_instruction=system)
            )
        except errors.APIError as exc:
            raise LLMUnavailableError(str(exc)) from exc
        return response.text or ""