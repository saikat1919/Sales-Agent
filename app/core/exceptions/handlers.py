from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions.errors import ConflictError, NotFoundError, LLMUnavailableError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(exc_class_or_status_code=NotFoundError)
    async def not_found(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(exc_class_or_status_code=ConflictError)
    async def conflict(_: Request, exc: ConflictError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(exc_class_or_status_code=LLMUnavailableError)
    async def llm_unavailable(_: Request, exc: LLMUnavailableError) -> JSONResponse:
        return JSONResponse(
            status_code=503,
            content={"detail": "The assistant is unavailable. Please try again later."},
        )