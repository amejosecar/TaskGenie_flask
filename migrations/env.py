# migrations/env.py

import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context

# Alembic Config object
config = context.config

# Logging setup
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Import Flask-SQLAlchemy db to get metadata
from app.extensions import db
target_metadata = db.metadata


def get_engine():
    """Obtain the SQLAlchemy engine from Flask-Migrate."""
    try:
        # Flask-SQLAlchemy < 3
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # Flask-SQLAlchemy >= 3
        return current_app.extensions['migrate'].db.engine


def run_migrations_offline():
    """Run migrations in 'offline' mode (without DB-API)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        render_as_batch=True,      # batch mode for SQLite
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode (with a live DB connection)."""
    # Skip empty auto-generated migrations
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = get_engine()
    raw_conf = current_app.extensions['migrate'].configure_args or {}
    conf_args = raw_conf.copy()
    # Remove any existing render_as_batch to avoid duplication
    conf_args.pop('render_as_batch', None)
    # Inject our directive handler
    conf_args['process_revision_directives'] = process_revision_directives

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,   # batch mode for SQLite
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
