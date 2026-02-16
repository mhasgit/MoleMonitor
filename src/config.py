"""App configuration. No env vars or secrets."""

APP_TITLE = "MoleMonitor"
PAGE_ICON = "🕵️"

# Sidebar navigation labels
NAV_PAGES = [
    "Home",
    "Register",
    "Login",
    "Forgot Password",
    "Instructions",
    "Image History",
    "About",
]

ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "webp", "bmp")

# Persistence (relative to project root)
DATA_DIR = "data"
UPLOADS_DIR = "data/uploads"
DB_PATH = "data/molemonitor.db"
