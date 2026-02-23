"""App configuration. No env vars or secrets."""

APP_TITLE = "MoleMonitor"
PAGE_ICON = "🕵️"

# Sidebar navigation labels (main flow first, then account)
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

# Persistence (relative to project root)
DATA_DIR = "data"
UPLOADS_DIR = "data/uploads"
DB_PATH = "data/molemonitor.db"
