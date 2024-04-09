import os

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from google import generativeai as genai

from .ai_search import GoogleGeminiResponseGenerator
from .core import ConversationSession, set_session, get_session, reset_session
from .speech_to_text import GoogleSpeechToTextAgent

FLAVOUR = os.environ.get("FLAVOUR", "development")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    socketio = SocketIO(app)

    if FLAVOUR == "production":
        app.config.from_object('righttoknow.configs.production.ProductionConfig')
    else:
        app.config.from_object('righttoknow.configs.development.DevelopmentConfig')

    genai.configure(api_key=app.config.get("GOOGLE_API_KEY"))

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=["GET"])
    def home():
        return render_template("index.html")

    @socketio.on('start_recording')
    def handle_start_recording_request(geolocation):
        print("START_RECORDING")
        if get_session() is None:
            session = ConversationSession(
                socket=socketio,
                speech_to_text_agent=GoogleSpeechToTextAgent(),
                response_generator=GoogleGeminiResponseGenerator(),
            )

            set_session(session=session)

    @socketio.on('stream')
    def handle_message(data, geolocation):
        print("STREAM")
        recommendation = get_session().process(chunk_data=data)

        if recommendation is not None:
            socketio.emit('recommendation', {'data': recommendation})

    @socketio.on('disconnect')
    def handle_disconnect_request():
        print("DISCONNECT")
        reset_session()

    @socketio.on('stop_recording')
    def handle_stop_recording_request():
        print("STOP_RECORDING")
        reset_session()

    return app
