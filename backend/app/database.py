import os
from pathlib import Path

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "loantrack")
DB_USER = os.getenv("DB_USER", "loantrack_user")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_MIN_CONNECTIONS = int(os.getenv("DB_MIN_CONNECTIONS", "2"))
DB_MAX_CONNECTIONS = int(os.getenv("DB_MAX_CONNECTIONS", "10"))


if not DB_PASSWORD:
    raise RuntimeError("DB_PASSWORD is not configured")


DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=DB_MIN_CONNECTIONS,
    max_size=DB_MAX_CONNECTIONS,
    open=False,
)


def open_pool() -> None:
    """Open the PostgreSQL connection pool."""
    pool.open()


def close_pool() -> None:
    """Close the PostgreSQL connection pool."""
    pool.close()


def check_database_connection() -> bool:
    """Return True when PostgreSQL is reachable."""
    try:
        with pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        return True

    except Exception:
        return False