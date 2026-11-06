from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
class Config:
    SECRET_KEY = 'agrosaber-demo-local-2026'
    DATABASE = BASE_DIR / 'database' / 'agrosaber.db'
