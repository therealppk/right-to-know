import uuid
from io import BytesIO

from flask_socketio import SocketIO
from pydub import AudioSegment

from .ai_search import BaseResponseGenerator
from .speech_to_text import GoogleSpeechToTextAgent

_session = None


def get_session():
    return _session


def set_session(session: "ConversationSession"):
    global _session
    _session = session


def reset_session():
    global _session
    _session = None


class ConversationSession:
    def __init__(self, socket: SocketIO, speech_to_text_agent: GoogleSpeechToTextAgent,
                 response_generator: BaseResponseGenerator):
        self._socket = socket

        self._uuid = uuid.uuid4()

        self._recognizer = speech_to_text_agent
        self._response_generator = response_generator

        self._transcript = ""
        self._audio_segment: AudioSegment = AudioSegment.empty()
        self._c = 0
        self._bytes_stream = BytesIO()

        self._prev_trim_ms = 0

    def _get_last_silence(self, silence_threshold=-50.0, chunk_size=10):
        assert chunk_size > 0

        trim_ms = len(self._audio_segment)

        while self._audio_segment[trim_ms - chunk_size:trim_ms].dBFS > silence_threshold and trim_ms > 0:
            trim_ms -= chunk_size

        return max(0, trim_ms)

    def process(self, chunk_data: str):
        new_audio_segment = AudioSegment(data=chunk_data, frame_rate=16000, channels=1, sample_width=2)
        self._audio_segment += new_audio_segment

        new_trim_ms = self._get_last_silence()

        if new_trim_ms == self._prev_trim_ms:
            return

        self._transcript += self._recognizer.transcribe(
            audio_stream=self._audio_segment[self._prev_trim_ms:new_trim_ms].raw_data
        )

        self._c += 1
        self._prev_trim_ms = new_trim_ms

        return self._response_generator.get_response(conversation=self._transcript)
