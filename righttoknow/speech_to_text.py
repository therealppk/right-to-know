from io import BytesIO
import traceback

import speech_recognition as sr


class BaseSpeechToTextAgent:
    def transcribe(self, audio_stream: BytesIO, verbose: bool = False):
        raise NotImplementedError()


class GoogleSpeechToTextAgent(BaseSpeechToTextAgent):
    def __init__(self):
        self._recognizer = sr.Recognizer()

    def transcribe(self, audio_stream: BytesIO, verbose: bool = False):
        try:
            audio_data = sr.AudioData(audio_stream, sample_rate=16000, sample_width=2)
            transcript = self._recognizer.recognize_google(audio_data)

            if verbose:
                print(transcript)

            return transcript

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            traceback.print_exception(e)

        return ""
