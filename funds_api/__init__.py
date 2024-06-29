"""Flask app entry point."""
from flask import Flask

from funds_api.bp import funds
from funds_api.database import init_db_command, init_db
from funds_api.scripts import create_schema, data_migration


def create_app():
    # create and configure the app
    init_db()
    app = Flask(__name__)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_schema)
    app.cli.add_command(data_migration)
    app.register_blueprint(funds.bp)

    return app