import httpx

from typing import List, Tuple

from fastapi import HTTPException, status
from sentence_transformers import SentenceTransformer
from langchain.schema import Document
from chromadb.types import Collection
from chromadb.api.types import QueryResult

from app.core.config import settings

class ChromaDbService:
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    @staticmethod
    async def get_or_create_collection(collection_name: str) -> Collection:
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(
                f"{settings.CHROMA_COLLECTIONS_BASE_URL}/{collection_name}",
                headers=settings.chroma_headers
            )
            if response.status_code == status.HTTP_200_OK:
                collection = Collection(**response.json())
                print("Collection:", collection)
                return collection
            elif response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]:
                create_data = {
                    "name": collection_name,
                    "metadata": {
                        "hnsw:search_ef": 50
                    }
                }
                create_response = await client.post(settings.CHROMA_COLLECTIONS_BASE_URL, json=create_data, headers=settings.chroma_headers)
                if create_response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
                    collection = Collection(**create_response.json())
                    print("New collection:", collection)
                    return collection
                else:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create collection: {create_response.status_code} - {create_response.text}")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create collection: {response.status_code} - {response.text}")
    
    @staticmethod
    async def collection_query(
        collection_id: str,
        question: str,
        n_results: int
    ) -> QueryResult:
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                f"{settings.CHROMA_COLLECTIONS_BASE_URL}/{collection_id}/query",
                json={
                    "query_embeddings": [
                        ChromaDbService.embedding_model.encode(question).tolist()
                    ],
                    "n_results": n_results,
                    "include": [
                        "metadatas",
                        "documents",
                        "distances"
                    ]
                },
                headers=settings.chroma_headers,
            )
            if response.status_code == status.HTTP_200_OK:
                result = QueryResult(**response.json())
                print("QueryResult:", result)
                return result
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get QueryResult: {response.status_code} - {response.text}")
        
