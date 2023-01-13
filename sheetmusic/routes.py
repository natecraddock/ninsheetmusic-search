import logging
import sqlite3

from flask import Blueprint, g, render_template, request

from sheetmusic.db import get_db

# probably don't need the last two...
routes = Blueprint("routes", __name__, static_folder="static", template_folder="templates")

def get_series() -> list[str]:
    db = get_db()
    try:
        series = db.execute("SELECT DISTINCT series FROM music ORDER BY series ASC").fetchall()
        if not series:
            return []
        return map(lambda x: x["series"], series)
    except sqlite3.OperationalError as e:
        logging.error(e)
        return []

def get_stats() -> tuple:
    db = get_db()
    try:
        metadata = db.execute("SELECT * FROM metadata").fetchone()
        return metadata["last_update"], metadata["num_sheets"]
    except sqlite3.OperationalError as e:
        logging.error(e)
        return "", 0

@routes.before_request
def get_base_data():
    series = get_series()
    last_update, num_sheets = get_stats()
    g.series = series
    g.last_update = last_update
    g.num_sheets = num_sheets

@routes.route("/")
def index():
    if not series:
        return render_template
    return render_template("index.html", series=series)

@routes.route("/series/<path:name>")
def series(name):
    db = get_db()
    sheets = db.execute("SELECT * FROM music WHERE series=? ORDER BY game, title", (name,))

    mapping = {}
    for sheet in sheets:
        if sheet["game"] in mapping:
            mapping[sheet["game"]].append(sheet)
        else:
            mapping[sheet["game"]] = [sheet]

    games = list(mapping.keys())

    return render_template("sheets.html", series=series, name=f"Series: {name}", sheets=mapping, games=games)

@routes.route("/search", methods=["POST"])
def search():
    query = request.form["query"]
    db = get_db()

    try:
        sheets = db.execute("SELECT * FROM music WHERE title LIKE ? OR game LIKE ?", (f"%{query}%", f"%{query}%"))
    except sqlite3.OperationalError as e:
        logging.error(e)
        sheets = []

    mapping = {}
    for sheet in sheets:
        if sheet["game"] in mapping:
            mapping[sheet["game"]].append(sheet)
        else:
            mapping[sheet["game"]] = [sheet]

    games = list(mapping.keys())

    return render_template("sheets.html", series=series, name=f"Search: {query}", sheets=mapping, games=games)
