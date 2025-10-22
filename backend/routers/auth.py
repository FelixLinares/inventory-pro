# backend/routers/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter()

class RegisterAdminIn(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/register-admin")
def register_admin(data: RegisterAdminIn):
    # TODO: lógica real con DB; por ahora simulamos OK
    return {"created": True, "email": data.email}

@router.post("/login")
def login(data: LoginIn):
    # TODO: validar contra DB; por ahora simulamos OK si hay password
    if not data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"token": "demo-token", "email": data.email}
