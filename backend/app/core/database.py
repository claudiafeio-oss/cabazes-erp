from sqlalchemy import Engine, create_engine
from collections.abc import Generator

from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


DATABASE_URL = (
    f"postgresql+psycopg://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)

_engine: Engine | None = None
SessionLocal = sessionmaker(autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator:
    db = SessionLocal(bind=get_engine())
    try:
        yield db
    finally:
        db.close()


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL, future=True)
    return _engine
