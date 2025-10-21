# Inventory Pro (Render + Supabase)

## Deploy rápido
1. Sube este repo a GitHub.
2. Crea base en **Supabase** (free) y copia `DATABASE_URL` (psycopg2) con `?sslmode=require`.
3. **Render → New Web Service** (root: `backend/`)
   - Build: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Variables: ver `backend/README.md`
4. **Render → New Static Site** (root: `frontend/`)
5. Abre `https://TU_FRONTEND.onrender.com/set-api.html` y pega la URL del backend.
6. (Solo 1 vez) `register.html` para crear admin. Luego inicia sesión en `login.html`.
