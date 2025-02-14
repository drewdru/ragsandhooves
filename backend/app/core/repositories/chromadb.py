import httpx

from fastapi import HTTPException, status
from sentence_transformers import SentenceTransformer
from chromadb.types import Collection
from chromadb.api.types import QueryResult, GetResult, DeleteRequest, AddRequest
from app.core.types.chromadb import GetRequestOptional, QueryRequestOptional

from app.core.config import settings

class ChromaDbRepository:
    """Encapsulates all ChromaDb-related CRUD operations."""
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
        filter_data: QueryRequestOptional,
        question: str | None = None,
    ) -> QueryResult:
        """Get Nearest Neighbors"""
        
        if filter_data.get("embeddings", None) is None and question is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="collection_query require question or filter_data['embeddings']")

        embeddings = filter_data.get("embeddings", [
            ChromaDbService.embedding_model.encode(question).tolist()
        ])
        n_results = filter_data.get("n_results", 20)
        include = filter_data.get("include", [
            "metadatas",
            "documents",
            "distances"
        ])
        
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                f"{settings.CHROMA_COLLECTIONS_BASE_URL}/{collection_id}/query",
                json={
                    **{k: v for k, v in filter_data.items() if k != "embeddings"},
                    "query_embeddings": embeddings,
                    "n_results": n_results,
                    "include": include
                },
                headers=settings.chroma_headers,
            )
            if response.status_code == status.HTTP_200_OK:
                result = QueryResult(**response.json())
                print("QueryResult:", result)
                return result
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get QueryResult: {response.status_code} - {response.text}")
        
    @staticmethod
    async def get_collection_documents(collection_id: str, filter_data: GetRequestOptional) -> GetResult:
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                f"{settings.CHROMA_COLLECTIONS_BASE_URL}/{collection_id}/get",
                json=filter_data,
                headers=settings.chroma_headers
            )
            if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
                documents = GetResult(**response.json())
                print("Documents:", documents)
                return documents
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get documents: {response.status_code} - {response.text}")

    @staticmethod
    async def delete_collection_documents(collection_id: str, filter_data: DeleteRequest) -> None:
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                f"{settings.CHROMA_COLLECTIONS_BASE_URL}/{collection_id}/delete",
                json=filter_data,
                headers=settings.chroma_headers
            )
            if response.status_code != status.HTTP_200_OK:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete documents: {response.status_code} - {response.text}")
    
    @staticmethod
    async def add_collection_documents(collection_id: str, data: AddRequest) -> None:
        add_url = f"{settings.CHROMA_COLLECTIONS_BASE_URL}/{collection_id}/add"
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                add_url,
                json=data,
                headers=settings.chroma_headers
            )
            if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to add documents: {response.status_code} - {response.text}")
    