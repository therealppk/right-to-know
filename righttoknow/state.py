import time
import os
from geopy.geocoders import Nominatim
from pydub import AudioSegment



class State:
    def __init__(self):
        self.values = 1
        self.time_now = time.time()
        self.first_prompt_flag = True
        self.val_file_name_for_run = 1
        self.test_out = None
        self.text_from_speech = ""
        os.makedirs(f"audio_recording/{self.time_now}/{self.val_file_name_for_run}")



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
        

    def update_val_file_name_for_run(self):
        self.test_out.export(f"audio_recording/{self.time_now}/{self.val_file_name_for_run}/testOut.wav", format="wav")
        self.text_from_speech = ""
        self.val_file_name_for_run += 1
        self.values = 0
        os.makedirs(f"audio_recording/{self.time_now}/{self.val_file_name_for_run}")