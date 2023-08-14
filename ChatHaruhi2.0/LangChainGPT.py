# LangChainGPT.py

from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, UserMessage, SystemMessage
from BaseLLM import BaseLLM

class LangChainGPT(BaseLLM):

    def __init__(self, model="gpt-3.5-turbo"):
        self.chat = ChatOpenAI(model=model)
        self.messages = []

    def initialize_message(self):
        self.messages = []

    def ai_message(self, payload):
        self.messages.append(AIMessage(payload))

    def system_message(self, payload):
        self.messages.append(SystemMessage(payload))

    def user_message(self, payload):
        self.messages.append(UserMessage(payload))

    def get_response(self):
        response = self.chat(self.messages)
        return response
    
    def print_prompt(self):
        for message in self.messages:
            print(message)
