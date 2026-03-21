from sentence_transformers import SentenceTransformer
import numpy as np

class SentenceTransformerModel:

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True
        )
        return np.array(embeddings).astype("float32")