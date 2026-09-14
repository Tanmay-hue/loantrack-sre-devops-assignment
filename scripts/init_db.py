from pathlib import Path
import os

import psycopg
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]

load_dotenv(ROOT / ".env")


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "loantrack")
DB_USER = os.getenv("DB_USER", "loantrack_user")
DB_PASSWORD = os.getenv("DB_PASSWORD")


if not DB_PASSWORD:
    raise RuntimeError("DB_PASSWORD is not configured")


DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


MIGRATION_FILE = ROOT / "db" / "migrations" / "001_create_loans.sql"
SEED_FILE = ROOT / "db" / "seed" / "001_seed_loans.sql"


def run_sql_file(connection, path: Path) -> None:
    sql = path.read_text(encoding="utf-8")

    with connection.cursor() as cursor:
        cursor.execute(sql)

    connection.commit()


def main() -> None:
    print("Connecting to PostgreSQL...")

    with psycopg.connect(DATABASE_URL) as connection:
        print(f"Applying migration: {MIGRATION_FILE.name}")
        run_sql_file(connection, MIGRATION_FILE)

        print(f"Applying seed data: {SEED_FILE.name}")
        run_sql_file(connection, SEED_FILE)

    print("Database initialization completed successfully.")


if __name__ == "__main__":
    main()