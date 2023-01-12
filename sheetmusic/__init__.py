import atexit
import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from sheetmusic.db import populate_db

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

    # load the instance config
    app.config.from_pyfile('config.py', silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import routes
    app.register_blueprint(routes.routes)

    def automation():
        with app.app_context():
            populate_db()

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=automation, trigger='cron', hour=0, minute=0)
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())

    return app
