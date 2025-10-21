# Backend (FastAPI)

**Variables en Render:**
- DATABASE_URL = postgresql+psycopg2://USER:PASSWORD@HOST:5432/DB?sslmode=require
- SECRET_KEY = una_cadena_larga_aleatoria
- ALGORITHM = HS256
- ACCESS_TOKEN_EXPIRE_MINUTES = 60
- ALLOWED_ORIGINS = https://TU_FRONTEND.onrender.com

**Local**
```
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```
