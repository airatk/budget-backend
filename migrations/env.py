from logging.config import fileConfig

from alembic import context
from alembic.config import Config
from sqlalchemy import MetaData, create_engine, pool
from sqlalchemy.engine import Engine

from core.databases.models.utilities.base import BaseModel
from core.settings import settings


# Alembic Config object to access the values within
# the .ini file in use.
config: Config = context.config

# Interpret the config file for Python logging,
# to set up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Model's MetaData object to support 'autogenerate'.
target_metadata: MetaData = BaseModel.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """

    context.configure(
        url=settings.POSTGRES_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    connectable: Engine = create_engine(
        url=settings.POSTGRES_URL,  # type: ignore [arg-type]
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
