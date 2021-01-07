import os
import logging

import click
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from tabulate import tabulate

from sodermalm import config
from sodermalm.database import Base, engine

logger = logging.getLogger(__name__)


@click.group()
def sodermalm_cli():
    """Command-line interface to Sodermalm."""
    pass


@sodermalm_cli.group('database')
def sodermalm_database():
    """Container for all Sodermalm database commands."""
    pass


def sync_triggers():
    from sqlalchemy_searchable import sync_trigger

    sync_trigger(engine, 'user', 'search_vector', ['email'])


@sodermalm_database.command('init')
def init_database():
    """Initializes a new database."""
    from sqlalchemy_utils import create_database, database_exists

    if not database_exists(str(config.SQLALCHEMY_DATABASE_URI)):
        create_database(str(config.SQLALCHEMY_DATABASE_URI))
    Base.metadata.create_all(engine)
    alembic_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'alembic.ini')
    alembic_cfg = AlembicConfig(alembic_path)
    alembic_command.stamp(alembic_cfg, 'head')

    sync_triggers()

    click.secho('Success.', fg='green')


@sodermalm_database.command('upgrade')
@click.option(
    '--tag', default=None, help="Arbitrary 'tag' name - can be used by custom env.py scripts."
)
@click.option(
    '--sql',
    is_flag=True,
    default=False,
    help="Don't emit SQL to database, dump to standard output instead"
)
@click.option('--revision', nargs=1, default='head', help='Revision identifier.')
def upgrade_database(tag, sql, revision):
    """Upgrades database schema to newest version."""
    from sqlalchemy_utils import database_exists, create_database
    from alembic.runtime.migration import MigrationContext

    alembic_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'alembic.ini')
    alembic_cfg = AlembicConfig(alembic_path)
    if not database_exists(str(config.SQLALCHEMY_DATABASE_URI)):
        create_database(str(config.SQLALCHEMY_DATABASE_URI))
        Base.metadata.create_all(engine)
        alembic_command.stamp(alembic_cfg, 'head')
    else:
        conn = engine.connect()
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()
        if not current_rev:
            Base.metadata.create_all(engine)
            alembic_command.stamp(alembic_cfg, 'head')
        else:
            alembic_command.upgrade(alembic_cfg, revision, sql=sql, tag=tag)

    sync_triggers()
    click.secho('Success', fg='green')


@sodermalm_database.command('heads')
def head_database():
    """Shows the heads of the database"""
    alembic_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'alembic.ini')
    alembic_cfg = AlembicConfig(alembic_path)
    alembic_command.heads(alembic_cfg)


@sodermalm_database.command('history')
def history_database():
    """Shows the history of the database"""
    alembic_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'alembic.ini')
    alembic_cfg = AlembicConfig(alembic_path)
    alembic_command.history(alembic_cfg)


@sodermalm_database.command("downgrade")
@click.option(
    "--tag", default=None, help="Arbitrary 'tag' name - can be used by custom env.py scripts."
)
@click.option(
    "--sql",
    is_flag=True,
    default=False,
    help="Don't emit SQL to database - dump to standard output instead.",
)
@click.option("--revision", nargs=1, default="head", help="Revision identifier.")
def downgrade_database(tag, sql, revision):
    """Downgrades database schema to next newest version."""
    alembic_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "alembic.ini")
    alembic_cfg = AlembicConfig(alembic_path)

    if sql and revision == "-1":
        revision = "head:-1"

    alembic_command.downgrade(alembic_cfg, revision, sql=sql, tag=tag)
    click.secho("Success.", fg="green")


@sodermalm_cli.group('server')
def sodermalm_server():
    """Container for all Sodermalm server commands."""
    pass


@sodermalm_server.command('config')
def show_config():
    """Prints thje current config as Sodermalm sees it."""
    import sys
    import inspect
    from sodermalm import config

    func_members = inspect.getmembers(sys.modules[config.__name__])

    table = []
    for key, value in func_members:
        if key.isupper():
            table.append([key, value])

    click.secho(tabulate(table, headers=['Key', 'Value']), fg='blue')


@sodermalm_server.command('routes')
def show_routes():
    """Prints all available routes."""
    from sodermalm.main import api_router

    table = []
    for r in api_router.routes:
        auth = False
        for d in r.dependencies:
            if d.dependency.__name__ == 'get_current_user':
                auth = True
        table.append([r.path, auth, ','.join(r.methods)])

    click.secho(tabulate(table, headers=['Path', 'Authenticated', 'Methods']), fg='blue')


def entry():
    try:
        sodermalm_cli()
    except Exception as e:
        click.secho(f'ERROR: {e}', bold=True, fg='red')


if __name__ == '__main__':
    entry()
