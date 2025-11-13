from datetime import datetime, timezone
from sqlmodel import Relationship, SQLModel, Field, func, DateTime, Column

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(primary_key=True, index=True, default=None)
    fullname: str
    username: str
    password: str
    is_inactive: bool = False

    # Audit fields
    created_at: datetime = Field(default_factory=lambda : datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(default_factory=lambda : datetime.now(tz=timezone.utc), sa_column=Column(DateTime(), onupdate=func.now()))
    is_deleted: bool = False

class Venue(SQLModel, table=True):
    __tablename__ = 'venues'

    id: int | None = Field(primary_key=True, index=True, default=None)
    url: str
    name: str
    acl_id: str = Field(index=True)
    volume_cnt: int
    
    # Audit fields
    created_at: datetime = Field(default_factory=lambda : datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(default_factory=lambda : datetime.now(tz=timezone.utc), sa_column=Column(DateTime(), onupdate=func.now()))
    is_deleted: bool = False

    # Relationships
    papers: list["Paper"] = Relationship(back_populates="venue")

class Paper(SQLModel, table=True):
    __tablename__ = "papers"

    id: int | None = Field(primary_key=True, index=True, default=None)
    s2_id: str | None = Field(index=True, default=None)
    url: str
    title: str
    authors: str
    abstract: str
    tldr: str | None = None
    venue_id: int | None = Field(default=None, index=True, foreign_key="venues.id")
    year: int | None = Field(default=None, index=True)

    # Audit fields
    created_at: datetime = Field(default_factory=lambda : datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(default_factory=lambda : datetime.now(tz=timezone.utc), sa_column=Column(DateTime(), onupdate=func.now()))
    is_deleted: bool = False

    # Relationships
    venue: Venue | None = Relationship(back_populates="papers")

class UserLikes(SQLModel, table=True):
    __tablename__ = "user_likes"

    id: int | None = Field(primary_key=True, index=True, default=None)
    user_id: int = Field(foreign_key="users.id", index=True)
    paper_id: int = Field(foreign_key="papers.id", index=True)

    # Audit fields
    created_at: datetime = Field(default_factory=lambda : datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(default_factory=lambda : datetime.now(tz=timezone.utc), sa_column=Column(DateTime(), onupdate=func.now()))
    is_deleted: bool = False

