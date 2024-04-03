import os

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from righttoknow.state import State

FLAVOUR = os.environ.get("FLAVOUR", "development")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    socketio = SocketIO(app)
    state_instance = State(socketio)

    if FLAVOUR == "production":
        app.config.from_object('righttoknow.configs.production.ProductionConfig')
    else:
        app.config.from_object('righttoknow.configs.development.DevelopmentConfig')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    @app.route("/", methods=["GET"])
    def home():
        return render_template("home.html")


    @socketio.on('connect')
    def handle_connect_request():
        print('request made')


    @socketio.on('stream')
    def handle_message(data, geolocation):
        state_instance.handle_message(data, geolocation)


    @app.route("/stop-recording", methods=['GET'])
    def update_val_file_name_for_run():
        return state_instance.update_val_file_name_for_run()
    

    return app