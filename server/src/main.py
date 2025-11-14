from contextlib import asynccontextmanager

from src.routes.papers import load_venues_from_db, router as papers_router
from src.routes.auth import router as auth_router
from src.core.settings import get_settings
from src.utils.logger import setup_logger
from src.core.db import alembic_upgrade

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()
logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Starting server...')    
    alembic_upgrade()
    logger.info('Database migrations applied...')

    # load Venues from DB to cache
    app.state.venues = load_venues_from_db(settings.db_url)
    logger.info(f'Loaded {len(app.state.venues)} venues into cache')
    yield

app = FastAPI(
    lifespan=lifespan
)

origins = [
    'http://localhost:5173',
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(papers_router, prefix='/api/v1/papers')
app.include_router(auth_router, prefix='/api/v1/auth')

@app.get('/api/health')
async def health_check():
    return {"status": "healthy"}

