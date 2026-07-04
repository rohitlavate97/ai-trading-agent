import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from core.config import settings

# Use local storage for vector DB in development mode
# This creates a "qdrant_data" folder in the backend directory
QDRANT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "qdrant_data")
COLLECTION_NAME = "company_filings"
VECTOR_SIZE = 1536 # Standard size for OpenAI text-embedding-ada-002

_qdrant_client = None

def get_qdrant_client() -> QdrantClient:
    """Returns a singleton QdrantClient instance, creating it if necessary."""
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(path=QDRANT_PATH)
        
        # Initialize collection if it doesn't exist
        collections = _qdrant_client.get_collections().collections
        if not any(c.name == COLLECTION_NAME for c in collections):
            _qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            )
            
            # Insert some dummy/mock data for testing the RAG pipeline
            _qdrant_client.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    {
                        "id": 1,
                        # A dummy vector
                        "vector": [0.01] * VECTOR_SIZE,
                        "payload": {
                            "symbol": "AAPL",
                            "document_type": "10-K",
                            "content": "Apple Inc. continues to face supply chain risks due to global semiconductor shortages, though demand for the latest iPhone models remains highly robust."
                        }
                    },
                    {
                        "id": 2,
                        "vector": [0.02] * VECTOR_SIZE,
                        "payload": {
                            "symbol": "TSLA",
                            "document_type": "10-Q",
                            "content": "Tesla's expansion into new gigafactories in Europe and Texas has significantly increased production capacity, lowering per-unit manufacturing costs."
                        }
                    }
                ]
            )
            
    return _qdrant_client
