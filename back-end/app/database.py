from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import NullPool, QueuePool
from app.config import settings


_SERVERLESS = settings.APP_ENV == "serverless"

_engine_kwargs: dict = {
    "pool_pre_ping": True,          
    "connect_args": {
        "sslmode": "require",       
        "connect_timeout": 10,
    },
}

if _SERVERLESS:
    _engine_kwargs["poolclass"] = NullPool
else:
    _engine_kwargs.update({
        "poolclass": QueuePool,
        "pool_size": 5,
        "max_overflow": 5,
        "pool_recycle": 270,
        "pool_timeout": 30,
    })

engine = create_engine(settings.DATABASE_URL, **_engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency que fornece uma sessão de banco e garante fechamento ao final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
