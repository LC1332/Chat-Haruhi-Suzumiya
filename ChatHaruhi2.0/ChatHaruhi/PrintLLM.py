# LangChainGPT.py

from .BaseLLM import BaseLLM

class PrintLLM(BaseLLM):

    def __init__(self ):
        self.messages = []
        self.messages.append("Noticing: This is a print LLM for debug.")
        self.messages.append("But you can also copy the prompt into GPT or Claude to debugging")

    def initialize_message(self):
        self.messages = []
        self.messages.append("Noticing: This is a print LLM for debug.")
        self.messages.append("But you can also copy the prompt into GPT or Claude to debugging")

    def ai_message(self, payload):
        self.messages.append("AI: \n" + payload)

    def system_message(self, payload):
        self.messages.append("System: \n" + payload)

    def user_message(self, payload):
        self.messages.append("User: \n" + payload)

    def get_response(self):
        for message in self.messages:
            print(message)
        response = input("Please input your response: ")
        return response
    
    def print_prompt(self):
        for message in self.messages:
            print(message)
