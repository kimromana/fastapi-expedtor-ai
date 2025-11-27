from logging.config import fileConfig
import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# =====================
# Загружаем .env
# =====================
load_dotenv(".env")

# =====================
# Настройка путей (чтобы импортировать app.*)
# =====================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

# =====================
# Импорт config и Base
# =====================
from app.core.config import settings
from app.db.base import Base  # Base.metadata используется Alembic

# =====================
# Alembic Config
# =====================
config = context.config

# Передаём URL базы из .env в alembic.ini
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные моделей (для автогенерации)
target_metadata = Base.metadata


# =====================
# Offline режим
# =====================
def run_migrations_offline() -> None:
    """Запуск миграций в оффлайн-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# =====================
# Online режим
# =====================
def run_migrations_online() -> None:
    """Запуск миграций в онлайн-режиме."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# =====================
# Запуск Alembic
# =====================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
