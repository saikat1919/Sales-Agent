from fastapi import APIRouter
from app.modules.catalog.controllers import router as catalog_router
from app.modules.chat.controllers import router as chat_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(router=catalog_router)
api_router.include_router(router=chat_router)