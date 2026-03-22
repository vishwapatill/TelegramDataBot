import numpy as np
from .Retriver import Retriver

class BruteForceRetriever(Retriver):
    def __init__(self, chunks, embeddings):
        self.chunks = chunks
        self.embeddings = np.array(embeddings).astype("float32")

        # Normalize once (important for cosine similarity)
        self.embeddings = self.embeddings / np.linalg.norm(
            self.embeddings, axis=1, keepdims=True
        )

    def get_top_k_chunks(self, query_embedding, k):
        query = np.array(query_embedding).astype("float32")
        query = query / np.linalg.norm(query)

        # Cosine similarity = dot product (after normalization)
        scores = np.dot(self.embeddings, query)

        # Get top-k indices
        top_k_idx = np.argsort(scores)[-k:][::-1]

        results = []
        for idx in top_k_idx:
            results.append((self.chunks[idx], float(scores[idx])))

        return results