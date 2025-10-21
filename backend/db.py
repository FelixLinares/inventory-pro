# backend/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings

Base = declarative_base()

# Construimos kwargs del engine
engine_kwargs = {"pool_pre_ping": True}

url = settings.DATABASE_URL.strip()

if url.startswith("postgres"):
    # Supabase/Render: forzar SSL
    engine_kwargs["connect_args"] = {"sslmode": "require"}
elif url.startswith("sqlite"):
    # Solo para uso local con SQLite
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(url, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from . import models  # asegura el registro de modelos
    Base.metadata.create_all(bind=engine)
