"""App configuration. Env overrides supported via os.environ."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load secrets for Flask: Vite does not inject client env into the API process.
_api_dir = Path(__file__).resolve().parent
_repo_root = _api_dir.parent
# Precedence: .env.local then .env (first one wins because override=False).
load_dotenv(_api_dir / ".env.local")
load_dotenv(_api_dir / ".env", override=False)
load_dotenv(_repo_root / "client" / ".env.local", override=False)
load_dotenv(_repo_root / "client" / ".env", override=False)

APP_TITLE = os.environ.get("APP_TITLE", "MoleMonitor")
PAGE_ICON = "🕵️"

NAV_PAGES = [
    "Home",
    "Image History",
    "Instructions",
    "About",
    "Register",
    "Login",
    "Forgot Password",
]

ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "webp", "bmp")

# Persistence (relative to project root = api/)
DATA_DIR = os.environ.get("DATA_DIR", "data")
UPLOADS_DIR = os.environ.get("UPLOADS_DIR", "data/uploads")
DB_PATH = os.environ.get("DB_PATH", "data/molemonitor.db")

# JWT (set JWT_SECRET in production)
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-only-change-in-production")
JWT_ACCESS_EXPIRATION_SECONDS = int(os.environ.get("JWT_ACCESS_EXPIRATION_SECONDS", str(7 * 24 * 60 * 60)))
JWT_RESET_EXPIRATION_SECONDS = int(os.environ.get("JWT_RESET_EXPIRATION_SECONDS", str(15 * 60)))
# URL: api/.env SUPABASE_URL wins over client/.env VITE_SUPABASE_URL (see load order above).
SUPABASE_URL = (
    os.environ.get("SUPABASE_URL", "").strip()
    or os.environ.get("VITE_SUPABASE_URL", "").strip()
    or os.environ.get("NEXT_PUBLIC_SUPABASE_URL", "").strip()
)
SUPABASE_SERVICE_ROLE_KEY = (
    os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    or os.environ.get("SUPABASE_KEY", "").strip()
    or os.environ.get("SUPABASE_ANON_KEY", "").strip()
    or os.environ.get("VITE_SUPABASE_ANON_KEY", "").strip()
    or os.environ.get("VITE_SUPABASE_PUBLISHABLE_KEY", "").strip()
    or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY", "").strip()
    or os.environ.get("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY", "").strip()
)
PASSWORD_RESET_REDIRECT_URL = os.environ.get("PASSWORD_RESET_REDIRECT_URL", "http://localhost:5173/forgot-password")

COMPARE_ALGO_VERSION = "phase1_heuristic_v1"

# Decision thresholds
DIAMETER_INCREASE_MM_THRESHOLD = float(os.environ.get("DIAMETER_INCREASE_MM_THRESHOLD", "1.0"))
AREA_CHANGE_PERCENT_THRESHOLD = float(os.environ.get("AREA_CHANGE_PERCENT_THRESHOLD", "20.0"))
COLOR_DELTAE_THRESHOLD = float(os.environ.get("COLOR_DELTAE_THRESHOLD", "6.0"))
IRREGULARITY_DELTA_THRESHOLD = float(os.environ.get("IRREGULARITY_DELTA_THRESHOLD", "2.0"))

# Preprocessing / quality
BLUR_DETECTION_LAPLACIAN_THRESHOLD = 100.0
EXPOSURE_LOW_L = 30.0
EXPOSURE_HIGH_L = 220.0

SEGMENT_MIN_MASK_AREA_PX = 100
COMPARE_MAX_PROCESSING_SIDE = int(os.environ.get("COMPARE_MAX_PROCESSING_SIDE", "1200"))
SEGMENT_MAX_MASK_AREA_RATIO = float(os.environ.get("SEGMENT_MAX_MASK_AREA_RATIO", "0.35"))
SEGMENT_CENTER_WEIGHT = float(os.environ.get("SEGMENT_CENTER_WEIGHT", "0.8"))
SEGMENT_SATURATION_WEIGHT = float(os.environ.get("SEGMENT_SATURATION_WEIGHT", "0.6"))
SEGMENT_DARKNESS_WEIGHT = float(os.environ.get("SEGMENT_DARKNESS_WEIGHT", "0.5"))
SEGMENT_COIN_PENALTY_WEIGHT = float(os.environ.get("SEGMENT_COIN_PENALTY_WEIGHT", "1.0"))

COIN_5P_DIAMETER_MM = float(os.environ.get("COIN_5P_DIAMETER_MM", "18.0"))
COIN_DETECT_MAX_SIDE = int(os.environ.get("COIN_DETECT_MAX_SIDE", "1024"))
COIN_DETECT_MAX_CONTOURS = int(os.environ.get("COIN_DETECT_MAX_CONTOURS", "60"))
