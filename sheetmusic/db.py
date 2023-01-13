import logging
import sqlite3

import click
from flask import current_app, g

from sheetmusic.scrape import scrape

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

def populate_db():
    db = get_db()

    data = scrape()
    if not data:
        return

    logging.info("clearing database")
    db.execute("DELETE FROM metadata")
    db.execute("DELETE FROM music")

    db.commit()

    logging.info("inserting data into database")
    db.executemany(
        "INSERT INTO music (title, game, series, platform, url) VALUES (?, ?, ?, ?, ?)",
        data["sheets"],
    )

    db.execute(
        "INSERT INTO metadata (last_update, num_sheets) VALUES (CURRENT_TIMESTAMP, ?)",
        (len(data["sheets"]),),
    )

    db.commit()
    logging.info("database updated")

    return True

@click.command("init-db")
def init_db_command():
    """Clear the existing data, create new tables, and populate with data"""
    init_db()
    populate_db()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
