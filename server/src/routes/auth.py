from src.utils.sec import hash, verify, create_token, AuthUser
from src.core.models import User
from src.core.db import DB

from sqlmodel import select
from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel


router = APIRouter(tags=["auth"])

class UserLogin(BaseModel):
    username: str
    password: str

class UserSignup(BaseModel):
    fullname: str
    username: str
    password: str

class UserPublic(BaseModel):
    fullname: str
    username: str
    is_inactive: bool = False

def get_user(username: str, db: DB) -> User | None:
    stmt = select(User).where(User.username == username)
    stmt = stmt.where(User.is_inactive == False) # noqa
    stmt = stmt.where(User.is_deleted == False) # noqa
    user = db.exec(stmt).first()
    return user

def add_user(user: User, db: DB):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_password(user: User, new_password: str, db: DB):
    user.password = hash(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
async def login(user: UserLogin, db: DB, response: Response):
    db_user = get_user(user.username, db)
    if not db_user or not verify(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_token({"user_id": db_user.id})
    response.set_cookie(key="token", value=token, httponly=True, secure=False, samesite="lax", max_age=10 * 365 * 24 * 60 * 60)
    return {"message": "Login successful", "token": token}

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup, db: DB):
    if get_user(user.username, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    user = User(fullname=user.fullname, username=user.username, password=hash(user.password))
    add_user(user, db)
    return {"message": "User created successfully"}


@router.put('/forgot-password')
async def forgot_password(user: UserLogin, db: DB, auth_user: AuthUser):
    existing_user = get_user(user.username, db)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if existing_user.id != auth_user['user_id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only reset your own password",
        )
    
    update_user_password(existing_user, user.password, db)
    return {"message": "Password reset"}

@router.get('/me')
async def me(auth_user: AuthUser, db: DB):
    user = db.get(User, auth_user['user_id'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserPublic.model_validate(user, from_attributes=True)

@router.post('/verify-token')
async def verify_token(auth_user: AuthUser):
    return {"message": "Token is valid"}