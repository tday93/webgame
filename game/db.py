import psycopg2
import psycopg2.extras

import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db():
    if 'db' not in g:
        conn = psycopg2.connect(**current_app.config["DATABASE"])
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        g.db = {"conn": conn, "cur": cursor}

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db["cur"].close()
        db["conn"].close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db["cur"].execute(f.read())
        db["conn"].commit()


def easy_query(query, values, db=None):
    if not db:
        db = get_db()
    db["cur"].execute(query, values)
    return db["cur"].fetchone()


def json_update(query, data, values, db=None):
    if not db:
        db = get_db()
    db["cur"].execute(query, [psycopg2.extras.Json(data)] + values)
    db["conn"].commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
