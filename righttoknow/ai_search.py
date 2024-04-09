import json

from google import generativeai as genai


class BaseResponseGenerator:
    def get_response(self, conversation: str, verbose: bool = False):
        raise NotImplementedError()


class GoogleGeminiResponseGenerator(BaseResponseGenerator):
    def __init__(self):
        self._gemini_model = genai.GenerativeModel('gemini-pro')
        self._gemini_chat = self._gemini_model.start_chat()

    def _get_prompt(self, conversation: str):
        return (
            f"The following is a conversation between me and a police officer.\n"
            f"{conversation}\n"
            f"Understand the context. Is there anything to be concerned about? Is there any law that protects me? "
            f"Give me an answer with maximum three bullet points. Each bullet point should contain what my right is "
            f"what I should do. The bullet point should be under 50 words."
            # f"Be specific about the details of the laws, put them in bullet points, and limit it to 200 words and "
            # f"point us to the government documents on the web that work as a proof.\n"
            f"Give the answer as a JSON of the format.\n"
            f"`{{\"is_important\": <boolean>, \"answer\": \"<answer>\"}}` where `is_important` tells me if I need to "
            f"be concerned and `answer` tells me the response which is JSON encoded."
        )

    def get_response(self, conversation: str, verbose: bool = False):
        response = self._gemini_chat.send_message(self._get_prompt(conversation))

        if verbose:
            print(response.text)

        output = "\n".join([line for line in response.text.split("\n") if not line.startswith("```")])
        print(output)
        output = json.loads(output)

        return output["answer"] if output["is_important"] is True else None
