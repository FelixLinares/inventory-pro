# backend/main.py
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from .settings import settings
from .db import SessionLocal, init_db
from .models import User

from passlib.context import CryptContext
import jwt  # PyJWT

# ---------------------------
# Configuración básica
# ---------------------------
API_TITLE = getattr(settings, "API_TITLE", "Inventory API")
API_VERSION = getattr(settings, "API_VERSION", "0.1.0")
SECRET_KEY = getattr(settings, "SECRET_KEY", "change-me-in-env")
JWT_ALG = "HS256"
ACCESS_TOKEN_MIN = 60 * 12  # 12h

app = FastAPI(title=API_TITLE, version=API_VERSION)

# CORS: front en Render y pruebas locales (agrega más si necesitas)
ALLOWED_ORIGINS = [
    "https://inventario-pro-front.onrender.com",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------------------
# Helpers DB
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# Esquemas (lo mínimo que usa el front)
# ---------------------------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------------------------
# Eventos / Health
# ---------------------------
@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/")
def root():
    return {"message": "Inventory API"}

# ---------------------------
# Auth
# ---------------------------
@app.post("/auth/register-admin", status_code=201)
def register_admin(payload: UserCreate, db: Session = Depends(get_db)):
    """Crea el primer usuario admin si aún no hay ninguno."""
    # ¿Ya existe al menos un usuario?
    any_user = db.query(User).first()
    if any_user:
        raise HTTPException(status_code=400, detail="Ya existe un usuario. Use login.")

    # ¿Email repetido?
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado.")

    hashed = pwd_context.hash(payload.password)
    u = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hashed,
        is_admin=True,
        is_active=True,
        failed_attempts=0,
        is_locked=False,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"id": u.id, "email": u.email, "is_admin": u.is_admin}

@app.post("/auth/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    """Login básico: devuelve JWT."""
    u = db.query(User).filter(User.email == payload.email).first()
    if not u:
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    if not pwd_context.verify(payload.password, u.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    now = datetime.utcnow()
    exp = now + timedelta(minutes=ACCESS_TOKEN_MIN)
    token = jwt.encode({"sub": str(u.id), "exp": exp}, SECRET_KEY, algorithm=JWT_ALG)

    return TokenOut(access_token=token)

