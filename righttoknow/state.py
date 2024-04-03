import time
import os
from geopy.geocoders import Nominatim
from pydub import AudioSegment
from flask import jsonify
from flask_socketio import SocketIO, emit
from .ai_search import Gemini
from .speech_to_text import SpeechToText

class State:
    def __init__(self, socketio):
        self.values = 1
        self.time_now = time.time()
        self.speech_to_text_engine = SpeechToText()
        self.gemini_bot = Gemini()
        self.first_prompt_flag = True
        self.val_file_name_for_run = 1
        self.test_out = None
        self.text_from_speech = ""
        os.makedirs(f"audio_recording/{self.time_now}/{self.val_file_name_for_run}")
        self.socketio = socketio


    def handle_message(self, data, geolocation):
        file_name = f"audio_recording/{self.time_now}/{self.val_file_name_for_run}/test{self.values}.wav"
        
        with open(file_name, "ab") as file:
            file.write(data)
        
        if self.values == 1:
            self.test_out = AudioSegment.from_wav(file_name)
            first_prompt_text = "The following is a conversation between a police officer and a driver. "
            if len(geolocation) != 0:
                latitude = geolocation['latitude']
                longitude = geolocation['longitude']
                geolocator = Nominatim(user_agent="myApp")
                location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True) 
                if location:
                    address_dict = location.raw['address']
                    state = address_dict.get('state', 'State not available')
                    county = address_dict.get('county', 'County not available')
                    first_prompt_text += f"This is taking place in {state} and {county} county. "
        
        else:
            self.test_out += AudioSegment.from_wav(file_name)
            first_prompt_text = ""
        
        self.text_from_speech += self.speech_to_text_engine.convert_speech_to_text(file_name)
        self.text_from_speech += "\n"

        prompt = f"""
            {first_prompt_text}
            Split up the following "Information" into sentences based on your understanding. 
            Write the split up sentences also in your response. 
            After which, there is a question, please answer that.
            
            Information:
            {self.text_from_speech}

            Is there any law that protects me? Be specific about the details of the laws, put them in bullet points, 
            and limit it to 400 words and point us to the government documents on the web that work as a proof. 
            """
        try:
            gemini_response = self.gemini_bot.ask_gemini(prompt)
            print(gemini_response)
        except:
            gemini_response = "No Valid Response"
            print("No Valid Response")

        self.socketio.emit('recommendation', {'data' : gemini_response})
        self.values += 1

        if os.path.exists(file_name):
            os.remove(file_name)

        return 
        
    def update_val_file_name_for_run(self):
        self.gemini_bot = Gemini()
        self.test_out.export(f"audio_recording/{self.time_now}/{self.val_file_name_for_run}/testOut.wav", format="wav")
        self.text_from_speech = ""
        self.val_file_name_for_run += 1
        self.values = 0
        os.makedirs(f"audio_recording/{self.time_now}/{self.val_file_name_for_run}")
        return jsonify({"msg:": "All OK"})