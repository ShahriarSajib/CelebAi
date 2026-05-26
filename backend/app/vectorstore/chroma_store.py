import chromadb
from sentence_transformers import SentenceTransformer


class ChromaStore:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaStore, cls).__new__(cls)
        return cls._instance

    def __init__(self):

        # Prevent re-initialization
        if hasattr(self, "initialized"):
            return

        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="celebrities"
        )

        # Load embedding model ONCE
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.initialized = True

    # =========================
    # ADD DOCUMENT
    # =========================
    def add_document(self, doc_id: str, text: str, metadata: dict = None):

        embedding = self.model.encode(text).tolist()

        # -----------------------------
        # SAFE METADATA CLEANING
        # -----------------------------
        clean_metadata = {}

        if metadata:
            for key, value in metadata.items():

                # Chroma only accepts str, int, float, bool
                if value is None:
                    continue

                if isinstance(value, (str, int, float, bool)):
                    clean_metadata[key] = value
                else:
                    clean_metadata[key] = str(value)

        # -----------------------------
        # ADD TO CHROMA
        # -----------------------------
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[clean_metadata]
        )

    # =========================
    # VECTOR SEARCH
    # =========================
    def search(self, query: str, top_k: int = 3):

        query_embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results