from flask import Flask

from server.database import database
from server.routes import blueprint, limiter, oauth


def create_app(config):
    app = Flask(__name__)
    app.config.update(config)

    @app.before_first_request
    def create_tables():
        database.alchemy.create_all()

    database.alchemy.init_app(app)
    limiter.init_app(app)
    oauth.init_app(app)
    oauth.register(
        name='auth',
        # hardcoded url go brrrrrrr
        server_metadata_url='https://auth.inpro.informatik.uni-freiburg.de/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        },
        client_id="HgUQw3xF2noPHiHviIgNxCee",
        # OMG another secrett!!! (nope,both is public :))
        client_secret="0GYLpTriEiV9tH8HDjcL6xoYwB0wh12Psv4j1gGkWrATzlsg"
    )

    app.register_blueprint(blueprint, url_prefix='')

    return app
