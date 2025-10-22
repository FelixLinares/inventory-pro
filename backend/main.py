from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from .db import init_db

app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}

from fastapi.middleware.cors import CORSMiddleware

# --- CORS: permitir el front y dev local ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://inventario-pro-front.onrender.com",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints de salud/diagnóstico ---
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}



@app.get('/')
def root():
    return {'ok': True}
