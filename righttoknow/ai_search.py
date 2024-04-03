import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

class Gemini():
  def __init__(self) -> None:
    self.model = genai.GenerativeModel('gemini-pro')
    self.gemini_chat = self.model.start_chat()
  
  def ask_gemini(self, conversation):
    response = self.gemini_chat.send_message(conversation)
    text = response.text

    to_extracat_from = ["**Answer:**", "proof.", "Assistant**", "Assistant:**"]
    
    for to_extract in to_extracat_from:
      if to_extract in text:
        
        index = text.rfind(to_extract)
        output = text[index+len(to_extract):]
        output = output.replace("*", "")

        return output
        
    text = text.replace("*", "")
    return text
  
