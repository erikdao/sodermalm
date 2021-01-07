import logging

import click
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


@sodermalm_database.command('init')
def init_database():
    """Initializes a new database."""
    from sqlalchemy_utils import create_database, database_exists

    if not database_exists(str(config.SQLALCHEMY_DATABASE_URI)):
        create_database(str(config.SQLALCHEMY_DATABASE_URI))
    Base.metadata.create_all(engine)

    click.secho('Success.', fg='green')


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


def entry():
    try:
        sodermalm_cli()
    except Exception as e:
        click.secho(f'ERROR: {e}', bold=True, fg='red')


if __name__ == '__main__':
    entry()
