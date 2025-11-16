from src.utils.logger import setup_logger
from src.utils.sec import AuthUser
from src.core.db import DB
from src.core.models import Paper, UserLikes, Venue

from fastapi import FastAPI, APIRouter, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import Session, create_engine, select, update

router = APIRouter(tags=["papers"])
logger = setup_logger(__name__)

class PaperFilters(BaseModel):
    offset: int = 0
    venue: str | None = None
    year: int | None = None
    user_id: str | None = None

def load_venues_from_db(db_url: str) -> dict[str, Venue]:
    stmt = select(Venue)
    with Session(create_engine(db_url)) as db:
        venues = db.exec(stmt).all()
    return {venue.acl_id: venue for venue in venues}

def get_papers(db: DB, 
               app: FastAPI,
               user_id: str,
               offset: int = None,
               venue: str | None = None,
               year: int | None = None,
               ):
    stmt = select(Paper)
    if venue:
        if venue_obj := app.state.venues.get(venue):
            stmt = stmt.where(Paper.venue_id == venue_obj.id)
        else:
            raise HTTPException(status_code=400, detail="Invalid venue")
    
    if year:
        stmt = stmt.where(Paper.year == year)
    liked_subquery = select(UserLikes.paper_id).where(
        UserLikes.user_id == user_id,
        UserLikes.is_deleted == False  # noqa
    )
    stmt = stmt.where(Paper.id.not_in(liked_subquery))
    stmt = stmt.limit(25)
    stmt = stmt.offset(offset)
    return db.exec(stmt).all()

def get_liked_papers(db: DB, auth_user: AuthUser):
    stmt = select(Paper)
    stmt = stmt.where(UserLikes.user_id == auth_user['user_id'])
    stmt = stmt.where(UserLikes.is_deleted == False) # noqa
    stmt = stmt.join(UserLikes, UserLikes.paper_id == Paper.id)
    return db.exec(stmt).all()

def like_paper(paper_id: str, user_id: str, db: DB):
    like = UserLikes(user_id=user_id, paper_id=paper_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

def unlike_paper(paper_id: int, user_id: int, db: DB):
    result = db.exec(
        update(UserLikes)
        .where(UserLikes.paper_id == paper_id, 
               UserLikes.user_id == user_id)
        .values(is_deleted=True)
    )
    if result.rowcount:
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Like not found")

@router.get('')
async def get_items(
    db: DB,
    auth_user: AuthUser,
    request: Request,
    offset: int = 0,
    venue_abbr: str | None = None,
    year: int | None = None,
    ) -> list[Paper]:
    return get_papers(
        offset=offset, 
        venue=venue_abbr, 
        year=year, 
        user_id=auth_user['user_id'],
        db=db,
        app=request.app
    )

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

@router.delete('/likes/{paper_id}', status_code=204)
async def remove_liked_paper(
    paper_id: int,
    db: DB,
    auth_user: AuthUser
    ) -> None:
    try:
        unlike_paper(paper_id=paper_id, user_id=int(auth_user['user_id']), db=db)
    except Exception as e:
        logger.error(f"Error unliking paper {paper_id} for user {auth_user['user_id']}: {e}")
        raise HTTPException(status_code=500, detail="Failed to unlike paper") from e