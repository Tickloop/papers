import os
from typing import Annotated
from fastapi import Depends

from src.core.settings import get_settings
settings = get_settings()

from sqlmodel import create_engine, Session
from alembic import command
from alembic.config import Config

engine = create_engine(settings.db_url)

def alembic_upgrade():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    alembic_ini = os.path.join(base_dir, 'alembic.ini')
    alembic_dir = os.path.join(base_dir, 'alembic')
    alembic_cfg = Config(alembic_ini)
    alembic_cfg.set_main_option('script_location', alembic_dir)
    command.upgrade(alembic_cfg, 'head')

def get_session():
    with Session(engine) as session:
        yield session

DB = Annotated[Session, Depends(get_session)]

