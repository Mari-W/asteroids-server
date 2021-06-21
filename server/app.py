from flask import Flask

from server.database import database
from server.routes import blueprint


def create_app(config):
    app = Flask(__name__)
    app.config.update(config)

    @app.before_first_request
    def create_tables():
        database.alchemy.create_all()

    database.alchemy.init_app(app)

    app.register_blueprint(blueprint, url_prefix='')

    return app
