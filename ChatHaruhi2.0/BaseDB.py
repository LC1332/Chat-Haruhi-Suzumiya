# BaseDB.py

from abc import ABC, abstractmethod

class BaseDB(ABC):

    @abstractmethod
    def init_db(self):
        pass
    
    @abstractmethod
    def save(self, file_path):
        pass

    @abstractmethod
    def load(self, file_path):
        pass

    @abstractmethod
    def search(self, vector, n_results):
        pass

    @abstractmethod
    def init_from_docs(self, vectors, documents):
        pass

    