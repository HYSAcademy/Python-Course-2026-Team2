from typing import List
from services.rag_service.providers.openai_provider import OpenAIEmbeddingProvider, openai_provider

class EmbeddingService:
    def __init__(self, provider: OpenAIEmbeddingProvider):
        self.provider = provider

    def embed_query(self, text: str) -> list[float]:
        vectors = self.provider.embed([text])
        return vectors[0]

    def embed_texts(self, texts: List[str], batch_size: int = 100) -> List[list[float]]:
        embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.provider.embed(batch)
            embeddings.extend(batch_embeddings)

        return embeddings

embedding_service = EmbeddingService(openai_provider)

