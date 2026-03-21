from abc import abstractmethod,ABC

class Retriver(ABC):
    @abstractmethod
    def get_top_k_chunks(self, query_embedding, k):
        """
        Returns:
            List of tuples: [(chunk, score), ...]
        """
        pass
    
