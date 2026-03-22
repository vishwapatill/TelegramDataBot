import pickle
import os
from .StorageBackend import StorageBackend

class PickleBackend(StorageBackend):
    def __init__(self, path):
        self.path = path

    def load(self):
        if not os.path.exists(self.path):
            return {"chunks": [], "embeddings": [], "meta": {}}

        with open(self.path, "rb") as f:
            return pickle.load(f)

    def save(self, chunks, embeddings, metadata):
        data = {
            "chunks": chunks,
            "embeddings": embeddings,
            "meta": metadata
        }
        with open(self.path, "wb") as f:
            pickle.dump(data, f)
    
    def get_all(self):
        return self.load()

    def clear(self):
        if os.path.exists(self.path):
            os.remove(self.path)