import chromadb
from .BaseDB import BaseDB
import random
import string
import os


class ChromaDB(BaseDB):
    def __init__(self):
        self.client = None
        self.collection = None
        self.path = None
    
    def init_db(self, folder_name=None):

        if self.client is not None:
            print('ChromaDB has already been initialized')
            return

        if folder_name is None:
            while os.path.exists(folder_name) or folder_name is None:
                # try to create a folder named temp_<random string> which is not yet existed
                folder_name = "tempdb_" + ''.join(random.sample(string.ascii_letters + string.digits, 8))

        self.path = folder_name
        self.client = chromadb.PersistentClient(path=folder_name)

        self.collection = self.client.get_or_create_collection("search")

    def save(self, file_path):
        if file_path != self.path:
            # copy all files in self.path to file_path, with overwrite
            os.system("cp -r " + self.path + " " + file_path)
            previous_path = self.path
            self.path = file_path
            self.client = chromadb.PersistentClient(path = file_path)
            # remove previous path if it start with tempdb
            if previous_path.startswith("tempdb"):
                os.system("rm -rf " + previous_path)

    def load(self, file_path):
        self.path = file_path
        self.client = chromadb.PersistentClient(path=file_path)
        self.collection = self.client.get_collection("search")

    def search(self, vector, n_results):
        results = self.collection.query(query_embeddings=[vector], n_results=n_results)
        return results['documents'][0]

    def init_from_docs(self, vectors, documents, folder_name=None):
        if self.client is None:
            self.init_db(folder_name)
        
        ids = []
        for i, doc in enumerate(documents):
            first_four_chat = doc[:min(4, len(doc))]
            ids.append(str(i) + "_" + first_four_chat)
        self.collection.add(embeddings=vectors, documents=documents, ids=ids)
        
