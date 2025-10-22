from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from .db import init_db
from .routers import auth  # si tu router de auth está en backend/routers/auth.py

app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

# 🔧 CORS: autoriza explícitamente tu front en Render
ALLOWED_ORIGINS = [
    "https://inventario-pro-front.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,           # evita '*' cuando allow_credentials=True
    allow_origin_regex=r"https://.*\.onrender\.com",  # comodín opcional
    allow_credentials=True,                  # cookies/headers de auth si algún día los usas
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}

# incluye tus routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
