# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Si estos imports existen en tu proyecto, se usarán.
# Si no existen, el try/except evita que crashee.
try:
    from .settings import settings
except Exception:
    class _S:
        API_TITLE = "Inventory API"
        API_VERSION = "0.1.0"
    settings = _S()

try:
    from .db import init_db
except Exception:
    def init_db():
        pass

app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

# ---------- CORS (¡LO IMPORTANTE!) ----------
ALLOWED_ORIGINS = [
    "https://inventario-pro-front.onrender.com",  # tu frontend en Render
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # mejor específico que '*'
    allow_credentials=False,
    allow_methods=["*"],            # GET, POST, PUT, DELETE, OPTIONS...
    allow_headers=["*"],            # Authorization, Content-Type, etc.
)
# --------------------------------------------

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/")
def root():
    return {"message": "Inventory API up"}

# Monta los routers si existen (auth con /auth/register-admin y /auth/login)
try:
    from .auth import router as auth_router
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
except Exception as e:
    print("auth router no cargado:", e)
