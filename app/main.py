from sqlalchemy import text
from fastapi import FastAPI, Depends
from app.api.v1.router import api_router
from app.core.config import Settings, get_settings
from app.core.exceptions.handlers import register_exception_handlers
from app.db.session import SessionDep

app = FastAPI(title=get_settings().APP_NAME)
register_exception_handlers(app)
app.include_router(router=api_router)

@app.get("/health")
async def health(settings: Settings = Depends(get_settings)) -> dict:
    return {"status": "ok", "app": settings.APP_NAME}

@app.get("/health/db")
async def db_health(session: SessionDep):
    result = await session.execute(text(text="SELECT version()"))
    version = result.scalar_one()
    ext = await session.execute(text(text="SELECT extname FROM pg_extension WHERE extname = 'vector';"))
    has_vector = ext.scalar_one_or_none() is not None

    return {
        "database": "connected",
        "version": version,
        "has_vector": "yes" if has_vector else "no"
    }