"""
db/migrations/env.py

Standard Alembic env.py, customized to:
  1. Load DATABASE_URL from the repo-root .env at runtime (not from
     alembic.ini), so there's one source of truth for credentials —
     the same .env Docker Compose uses.
  2. Point `target_metadata` at our actual ORM models (db/models), so
     `alembic revision --autogenerate` can diff the live database against
     the models and generate migrations for any drift.
"""
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# Make `db.*` importable when Alembic is run from inside db/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from db.models import Base  # noqa: E402  (import after sys.path fix)

# Load repo-root .env
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_REPO_ROOT / ".env")

config = context.config

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    raise RuntimeError(
        "DATABASE_URL not set — copy .env.example to .env at the repo root first."
    )
config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This is what makes `--autogenerate` possible.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
