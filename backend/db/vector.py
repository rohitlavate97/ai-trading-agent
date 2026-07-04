from qdrant_client import AsyncQdrantClient
from core.config import settings

# Global asynchronous Qdrant client
qdrant_client = AsyncQdrantClient(url=settings.QDRANT_URL)

async def init_vector_db():
    """
    Initialize Qdrant collections if they don't exist.
    Will be expanded in the RAG milestone.
    """
    # Example for future:
    # await qdrant_client.create_collection(
    #     collection_name="company_filings",
    #     vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    # )
    pass
