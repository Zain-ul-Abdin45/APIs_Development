from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.mongo import close_mongo
from app.db.postgres import close_postgres
from app.services.exchange_service import close_http_client
from app.routes import account


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup — connections are lazily initialised on first use,
    # so nothing to open explicitly here.
    yield
    # Shutdown — release all connection pools cleanly
    await close_mongo()
    await close_postgres()
    await close_http_client()


app = FastAPI(
    title="Async Account Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account.router)
