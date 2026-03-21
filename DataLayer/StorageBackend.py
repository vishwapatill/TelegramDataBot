from abc import ABC, abstractmethod

class StorageBackend(ABC):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self, chunks, embeddings, metadata):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def clear(self):
        pass