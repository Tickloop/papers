from contextlib import asynccontextmanager

from src.routes.items import router as items_router
from src.core.settings import get_settings
from src.utils.logger import setup_logger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()
logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Starting server...')
    yield

app = FastAPI(
    lifespan=lifespan
)

origins = [
    '*',
    'http://localhost:5173',
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(items_router, prefix='/v1/items')

@app.get('/health')
async def health_check():
    return {"status": "healthy"}

