"""App configuration. No env vars or secrets."""

APP_TITLE = "MoleMonitor"
PAGE_ICON = "🕵️"

# Sidebar navigation (main app only; auth pages are not in sidebar)
SIDEBAR_PAGES = [
    "Dashboard",
    "Home",
    "Image History",
    "Instructions",
    "About",
]

# Auth sub-pages when unauthenticated (Login, Register, Forgot)
AUTH_PAGES = ["Login", "Register", "Forgot Password"]

# Legacy: full nav list for any backward compatibility
NAV_PAGES = SIDEBAR_PAGES + AUTH_PAGES

ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "webp", "bmp")

# Persistence (relative to project root)
DATA_DIR = "data"
UPLOADS_DIR = "data/uploads"
DB_PATH = "data/molemonitor.db"
