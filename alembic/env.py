from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from backend.database import Base
from backend import models
from backend.database import Base
from backend.models import medication, vitals, symptom, user
target_metadata = Base.metadata



# Alembic Config
config = context.config

# Setup Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Set this to your Base's metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
