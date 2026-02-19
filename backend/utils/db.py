import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import quote_plus

# -------------------------------------------------
# Load .env explicitly from backend folder
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

if not env_path.exists():
    raise RuntimeError(f".env file not found at expected location: {env_path}")

load_dotenv(dotenv_path=env_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_NAME]):
    raise RuntimeError(
        "Database environment variables are not set properly. "
        "Check backend/.env file."
    )

# Safely encode password (important if it contains special characters)
DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
    echo=os.getenv("SQL_ECHO", "False") == "True"
)

# Optional: Test DB connection immediately on startup
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("✅ Database connection established successfully.")
except Exception as e:
    raise RuntimeError(f"❌ Database connection failed: {str(e)}")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db_session():
    return SessionLocal()