from abc import ABC, abstractmethod

class BaseLLM(ABC):

    def __init__(self):
        pass
    
    @abstractmethod
    def initialize_message(self):
        pass

    @abstractmethod    
    def ai_message(self, payload):
        pass

    @abstractmethod
    def system_message(self, payload):
        pass

    @abstractmethod
    def user_message(self, payload):
        pass

    @abstractmethod
    def get_response(self):
        pass

    @abstractmethod
    def print_prompt(self):
        pass


