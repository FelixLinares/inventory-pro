from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from .settings import settings
from .db import SessionLocal
from . import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def hash_password(password: str) -> str: return pwd_context.hash(password)
def verify_password(plain, hashed) -> bool: return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_minutes: int = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def get_current_user(token: str = Depends(oauth2_scheme)) -> models.User:
    from .db import SessionLocal
    db = SessionLocal()
    try:
        payload = decode_token(token)
        user_id: int = int(payload.get("sub"))
        user = db.get(models.User, user_id)
        if not user or not user.is_active: raise HTTPException(status_code=401, detail="Usuario inactivo")
        return user
    finally:
        db.close()

def admin_required(user: models.User = Depends(get_current_user)):
    if not user.is_admin: raise HTTPException(status_code=403, detail="Solo admin")
    return user
