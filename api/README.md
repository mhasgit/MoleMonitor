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
