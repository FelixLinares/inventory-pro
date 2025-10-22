from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from .db import init_db

# 👇 IMPORTA el router
from .routers.auth import router as auth_router

app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

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

@app.get("/")
def root():
    return {"ok": True}

# 👇 INCLUYE el router con prefijo /auth
app.include_router(auth_router, prefix="/auth", tags=["auth"])
