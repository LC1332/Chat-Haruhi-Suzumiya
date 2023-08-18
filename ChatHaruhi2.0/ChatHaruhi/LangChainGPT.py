# LangChainGPT.py

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from .BaseLLM import BaseLLM

class LangChainGPT(BaseLLM):

    def __init__(self, model="gpt-3.5-turbo"):
        super(LangChainGPT,self).__init__()
        self.chat = ChatOpenAI(model=model)
        self.messages = []

    def initialize_message(self):
        self.messages = []

    def ai_message(self, payload):
        self.messages.append(AIMessage(content = payload))

    def system_message(self, payload):
        self.messages.append(SystemMessage(content = payload))

    def user_message(self, payload):
        self.messages.append(HumanMessage(content = payload))

    def get_response(self):
        response = self.chat(self.messages)
        return response
    
    def print_prompt(self):
        for message in self.messages:
            print(message)
