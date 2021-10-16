from sqlalchemy import create_engine

from app.settings import settings

engine = create_engine(settings.db_uri())
