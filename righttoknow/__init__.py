import os

from flask import Flask


FLAVOUR = os.environ.get("FLAVOUR", "development")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if FLAVOUR == "production":
        app.config.from_object('righttoknow.configs.production.ProductionConfig')
    else:
        app.config.from_object('righttoknow.configs.development.DevelopmentConfig')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
