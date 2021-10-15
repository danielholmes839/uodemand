from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from .engine import engine

Session = sessionmaker()
Session.configure(bind=engine)


# db: Session = Depends(db_provider)
def db_provider():
    try:
        session = Session()
        yield session
    finally:
        session.close()


@contextmanager
def db_context():
    try:
        session = Session()
        yield session
    finally:
        session.close()
