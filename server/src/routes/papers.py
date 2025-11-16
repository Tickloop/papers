from src.utils.logger import setup_logger
from src.utils.sec import AuthUser
from src.core.db import DB
from src.core.models import Paper, UserLikes, Venue

from fastapi import FastAPI, APIRouter, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import Session, create_engine, select

router = APIRouter(tags=["papers"])
logger = setup_logger(__name__)

class PaperFilters(BaseModel):
    offset: int = 0
    venue: str | None = None
    year: int | None = None

def load_venues_from_db(db_url: str) -> dict[str, Venue]:
    stmt = select(Venue)
    with Session(create_engine(db_url)) as db:
        venues = db.exec(stmt).all()
    return {venue.acl_id: venue for venue in venues}

def get_papers(filters: PaperFilters, db: DB, app: FastAPI):
    stmt = select(Paper)
    logger.info(f"Filters: {filters}")
    logger.info(f"Available venues: {app.state.venues.keys()}")
    if filters.venue:
        if venue := app.state.venues.get(filters.venue):
            logger.info(f"Filtering by venue: {venue}")
            stmt = stmt.where(Paper.venue_id == venue.id)
        else:
            raise HTTPException(status_code=400, detail="Invalid venue")
    
    if filters.year:
        stmt = stmt.where(Paper.year == filters.year)
    stmt = stmt.limit(25)
    stmt = stmt.offset(filters.offset)
    return db.exec(stmt).all()

def get_liked_papers(db: DB, auth_user: AuthUser):
    stmt = select(Paper)
    stmt = stmt.where(UserLikes.user_id == auth_user['user_id'])
    stmt = stmt.join(UserLikes, UserLikes.paper_id == Paper.id)
    return db.exec(stmt).all()

def like_paper(paper_id: str, user_id: str, db: DB):
    like = UserLikes(user_id=user_id, paper_id=paper_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

@router.get('')
async def get_items(
    db: DB,
    auth_user: AuthUser,
    request: Request,
    offset: int = 0,
    venue_abbr: str | None = None,
    year: int | None = None,
    ) -> list[Paper]:
    return get_papers(PaperFilters(offset=offset, venue=venue_abbr, year=year), db, app=request.app)

@router.get('/likes')
async def get_liked_items(db: DB, auth_user: AuthUser):
    return get_liked_papers(db, auth_user)

class LikeRequest(BaseModel):
    action: str
    id: int

@router.post('')
async def action(
    like_request: LikeRequest, 
    db: DB,
    auth_user: AuthUser
    ) -> None:
    if like_request.action == 'accept':
        like_paper(like_request.id, auth_user['user_id'], db)
    