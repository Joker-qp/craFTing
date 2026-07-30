from pathlib import Path

APP_DIR = Path.home() / ".config" / "crafting"
DB_PATH = APP_DIR / "crafting.db"

def ensure_app_dir_exists():
    APP_DIR.mkdir(parents=True, exist_ok=True)