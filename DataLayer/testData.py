from DataManager import DataManager
from BruteForceretriver import BruteForceRetriever
from PickleStore import PickleBackend
from SentenceTransformerModel import SentenceTransformerModel



embed_model=SentenceTransformerModel()
db=PickleBackend('store.pkl')
dm=DataManager('./myKnowledge',db,embed_model)

# print(dm.sync())
# print(dm.is_synced())
print(db.get_all())
