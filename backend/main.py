from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from .db import init_db

# 👇 Asegúrate de que esto exista y apunte al archivo correcto
from .routers import auth

app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

# CORS correcto
ALLOWED_ORIGINS = [
    "https://inventario-pro-front.onrender.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}

# 👇 ESTO ES CLAVE: incluye el router de auth con el prefijo /auth
app.include_router(auth.router, prefix="/auth", tags=["auth"])
