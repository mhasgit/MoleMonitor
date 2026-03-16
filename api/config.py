"""App configuration. Env overrides supported via os.environ."""

import os

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
