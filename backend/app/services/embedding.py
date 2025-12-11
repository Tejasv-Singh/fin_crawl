from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

class EmbeddingService:
    def __init__(self):
        # Load local model (CPU friendly)
        # all-MiniLM-L6-v2 is fast and small
        print("Loading Embedding Model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def split_text(self, text: str) -> List[str]:
        return self.text_splitter.split_text(text)

    def embed_query(self, text: str) -> List[float]:
        # ChromaDB handles embedding generation automatically if we don't provide it, 
        # BUT we are using the explicit model here?
        # Actually, Chroma's default embedding function IS all-MiniLM-L6-v2 (onnx).
        # However, to have control, we can do it explicitly or let Chroma do it.
        # Implementation Plan said "Logic to load model".
        # If we pass `documents` to Chroma (as we did in vector_db.py), Chroma uses its default embedding function.
        # So we might not strictly need to compute embeddings HERE if we let Chroma do it.
        # BUT, the plan said "Embedding Pipeline (Chunking + Embeddings)".
        # Let's keep the chunks here.
        # For the sake of the plan, let's allow explicit embedding or just text splitting.
        
        # If we want to query with vector, we need this.
        return self.model.encode(text).tolist()

embedding_service = EmbeddingService()
