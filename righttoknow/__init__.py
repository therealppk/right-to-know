import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from righttoknow.state import State

FLAVOUR = os.environ.get("FLAVOUR", "development")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    socketio = SocketIO(app)
    state_instance = State()

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
    
    @app.route("/stop-recording", methods=['GET'])
    def update_val_file_name_for_run():
        state_instance.update_val_file_name_for_run()
        return jsonify({"msg:": "All OK"})
    

    return app