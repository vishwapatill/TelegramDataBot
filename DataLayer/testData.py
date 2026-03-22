from DataManager import DataManager
from BruteForceretriver import BruteForceRetriever
from PickleStore import PickleBackend
from SentenceTransformerModel import SentenceTransformerModel

def test_data_manager():
    # Initialize components
    embed_model = SentenceTransformerModel()
    db = PickleBackend('store.pkl')
    dm = DataManager('./myKnowledge', db, embed_model)

    # 1. Check Sync
    print("=== Checking Sync Status ===")
    is_synced = dm.is_synced()
    print(f"Is synced: {is_synced}")

    # 2. Sync
    print("\n=== Syncing Data ===")
    sync_result = dm.sync()
    print(f"Sync result: {sync_result}")

    # 3. Get Data
    print("\n=== Getting All Data ===")
    data = db.get_all()
    print(f"Number of chunks: {len(data['chunks'])}")
    print(f"Number of embeddings: {len(data['embeddings'])}")
    print(f"Metadata: {data['meta']}")

    # 4. Get Top-k for a Query
    print("\n=== Retrieving Top-k Chunks for a Query ===")
    if len(data['chunks']) > 0 and len(data['embeddings']) > 0:
        retriever = BruteForceRetriever(data['chunks'], data['embeddings'])
        query = "What are the eco-friendly materials used in t-shirts?"
        query_embedding = embed_model.encode([query])[0]
        top_k = 2
        results = retriever.get_top_k_chunks(query_embedding, top_k)
        print(f"Top {top_k} results for query: '{query}'")
        for i, (chunk, score) in enumerate(results, 1):
            print(f"\nResult {i} (Score: {score:.4f}):\n{chunk}...")
    else:
        print("No data available for retrieval.")

if __name__ == "__main__":
    test_data_manager()
