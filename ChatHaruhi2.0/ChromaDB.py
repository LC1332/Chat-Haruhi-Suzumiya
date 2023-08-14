import chromadb
from BaseDB import BaseDB

class ChromaDB(BaseDB):
    
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = None
    
    def init_db(self):
        self.collection = self.client.get_or_create_collection("search")

    def save(self, file_path):
        self.client.save(file_path)

    def load(self, file_path):
        self.client.load(file_path)
        self.collection = self.client.get_collection("search")

    def search(self, vector, n_results):
        results = self.collection.query(query_embeddings=[vector], n_results=n_results)
        return results['documents']

    def init_from_docs(self, vectors, documents):
        self.collection.add(embeddings=vectors, documents=documents)
        
