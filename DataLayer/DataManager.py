import os
import hashlib

class DataManager:

    def __init__(self, file_path, backend, embed_model,chunkSize=300,overlap=50):
        self.file_path = file_path
        self.backend = backend
        self.model = embed_model
        self.chunkSize=chunkSize
        self.overlap=overlap

    # Create hash of all files (health check)
    def _compute_hash(self):
        hash_md5 = hashlib.md5()

        for root, _, files in os.walk(self.file_path):
            for f in sorted(files):
                full_path = os.path.join(root, f)
                with open(full_path, "rb") as file:
                    hash_md5.update(file.read())

        return hash_md5.hexdigest()

    # Read all files
    def _load_files(self):
        texts = []
        for f in os.listdir(self.file_path):
            with open(os.path.join(self.file_path, f), "r", encoding="utf-8") as file:
                texts.append(file.read())
        return texts

    #  Chunking
    def _chunk(self, text):
        chunks = []
        for i in range(0, len(text), self.chunkSize - self.overlap):
            chunks.append(text[i:i+self.chunkSize])
        return chunks

    # Health check
    def is_synced(self):
        data = self.backend.load()
        stored_hash = data.get("meta", {}).get("hash")

        current_hash = self._compute_hash()
        return stored_hash == current_hash

    # Update DB
    def update(self):
        print("Updating database...")

        texts = self._load_files()

        all_chunks = []
        for t in texts:
            all_chunks.extend(self._chunk(t))

        embeddings = self.model.encode(all_chunks)

        metadata = {
            "hash": self._compute_hash(),
            "num_chunks": len(all_chunks)
        }

        self.backend.save(all_chunks, embeddings, metadata)

        print("Update complete.")

    # Ensure sync
    def sync(self):
        if not self.is_synced():
            print("Data out of sync. Rebuilding...")
            self.update()
        else:
            print("Data already in sync.")