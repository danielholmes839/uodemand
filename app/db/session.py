from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from .engine import engine

SessionMaker = sessionmaker()
SessionMaker.configure(bind=engine)


# db: Session = Depends(db_provider) FastAPI dependency injection
def db_provider():
    try:
        session = SessionMaker()
        yield session
    finally:
        session.close()


@contextmanager
def db_context():
    try:
        session = SessionMaker()
        yield session
    finally:
        session.close()
