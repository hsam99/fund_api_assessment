"""Database adaptor module."""
import json
import os
import pathlib

import click

from .json_db import JsonDb

DATA_FILE = pathlib.Path(__file__).parent.parent / 'data.json'

def get_db():
    """Returns the database instance such that it is accessible by multiple functions."""
    db = JsonDb()
    db.connect(DATA_FILE)

    return db


def init_db():
    """Creates the database JSON file if not exists."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as handler:
            json.dump({}, handler, indent=4)


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the JSON database.')
