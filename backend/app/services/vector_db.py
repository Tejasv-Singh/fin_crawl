import chromadb
from chromadb.config import Settings
from app.core.config import settings
from typing import List, Dict, Any

class VectorDBService:
    def __init__(self):
        # Persistent local client
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="fincrawl_docs",
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(self, chunks: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """
        Add chunks to the collection.
        """
        if not chunks:
            return
            
        self.collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """
        Query the collection.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

    def count(self):
        return self.collection.count()

vector_db = VectorDBService()
