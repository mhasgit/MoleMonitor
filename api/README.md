# MoleMonitor API (backend)

Flask API for the mole comparison pipeline: pairs CRUD, compare, reports.

## Setup

```bash
cd api
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

API base: `http://localhost:5000`

- `GET /api/health` — health check
- `GET /api/pairs` — list pairs
- `POST /api/pairs` — create pair (multipart: image_a, image_b, pair_name, filename_a, filename_b)
- `GET /api/pairs/<id>` — get pair
- `DELETE /api/pairs/<id>` — delete pair
- `DELETE /api/pairs` — clear all pairs
- `POST /api/compare` — run comparison (multipart: image_a, image_b; form: scale_mm, use_clahe, blur_kernel_size)
- `GET /api/pairs/<id>/reports` — list reports for pair
- `POST /api/pairs/<id>/reports` — save report (JSON body: { snapshot: {...} })
- `GET /uploads/<path>` — serve uploaded images

Env: `PORT`, `FLASK_DEBUG`, `CORS_ORIGINS`, `DATA_DIR`, `DB_PATH`, `UPLOADS_DIR`.

On startup, Flask loads `api/.env` then `client/.env` (without overriding keys already set in `api/.env`). **`client/.env` alone is not enough for password reset:** you must set `SUPABASE_SERVICE_ROLE_KEY` in `api/.env` (or the shell). You can copy `api/.env.example` to `api/.env`.

## Password reset email via Supabase

To send password reset links through Supabase, set these variables (see `api/.env.example`):

- `SUPABASE_URL` (or only `VITE_SUPABASE_URL` in `client/.env` — the API will use it as a fallback)
- `SUPABASE_SERVICE_ROLE_KEY` (service-role key from Supabase Dashboard → Settings → API; **never** put this in frontend env)
- `PASSWORD_RESET_REDIRECT_URL` (frontend URL users land on after clicking email link, default: `http://localhost:5173/forgot-password`)

Flow:

1. Client calls `POST /api/auth/forgot/verify-email`.
2. On account registration, API attempts to mirror the user into Supabase Auth.
3. API generates a short-lived app reset token and appends it to `PASSWORD_RESET_REDIRECT_URL` as `reset_token`.
4. API requests Supabase Auth to send the reset email.
5. User opens link and resets password on `/forgot-password`.

### Supabase URL settings (avoid wrong port and `otp_expired`)

The dev app from `npm start` is **Vite on port 5173**, not `3000`.

In **Supabase Dashboard → Authentication → URL Configuration**:

- Set **Site URL** to `http://localhost:5173` (or your real deployed origin).
- Under **Redirect URLs**, add at least:
  - `http://localhost:5173/forgot-password`
  - `http://localhost:5173/**` (optional wildcard for local dev)

Set `PASSWORD_RESET_REDIRECT_URL` in `api/.env` to the same host and path (default is already `http://localhost:5173/forgot-password`).

If the email still opens `localhost:3000`, Supabase is using an old Site URL — update it, send yourself a **new** reset email, and click the new link promptly (links expire quickly).
