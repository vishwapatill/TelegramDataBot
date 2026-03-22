from DataLayer.BruteForceretriver import BruteForceRetriever
from DataLayer.DataManager import DataManager
from DataLayer.PickleStore import PickleBackend
from DataLayer.SentenceTransformerModel import SentenceTransformerModel

from LLMLayer.OllamaLLM import OllamaLLM
from promptLogger import PromptLogger

from MainBot import RAGBot

import os


def main():
    # ---------- Paths ----------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    knowledge_path = os.path.join(BASE_DIR, "MyKnowledge")  # fix spelling if needed
    store_path = os.path.join(BASE_DIR, "store.pkl")

    # ---------- Models ----------
    embed_model = SentenceTransformerModel()
    llm = OllamaLLM("mistral", base_url="http://localhost:11434")

    # ---------- Storage ----------
    db = PickleBackend(path=store_path)
    dm = DataManager(knowledge_path, db, embed_model, chunkSize=400, overlap=100)

    # ---------- Sync Data ----------
    if not dm.is_synced():
        print("🔄 Syncing data...")
        dm.sync()
    else:
        print("✅ Data already in sync")

    # ---------- Load Data ----------
    data = db.get_all()

    if len(data["chunks"]) == 0:
        print("❌ Error: No data found in store")
        return

    # ---------- Retriever ----------
    retriever = BruteForceRetriever(data["chunks"], data["embeddings"])

    # ---------- Logger ----------
    logger = PromptLogger()

    # ---------- Bot ----------
    bot = RAGBot(llm, retriever, embed_model, logger)

    # ---------- Test Query ----------
    user_query = "What is the return policy?"

    print("\n🧠 User Query:", user_query)

    response = bot.answer_query(
        user_id="user_1",
        session_id="session_1",
        user_query=user_query
    )

    print("\n🤖 Response:\n")
    print(response)


if __name__ == "__main__":
    main()