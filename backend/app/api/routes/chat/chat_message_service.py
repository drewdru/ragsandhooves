import asyncio
from app.core.services.reranking.reranking_cohere import RerankingCohereService
from fastapi import APIRouter, HTTPException, status


router = APIRouter(prefix="/chat_message", tags=["chat"])

class ChatMessageService:
    @staticmethod
    async def create_message(
        reranking_client, model, top_n, query, documents
        ):
        message = await RerankingCohereService().rerank_documents(
            reranker=reranking_client, 
            model=model, 
            query=query, 
            documents=documents, 
            top_n=top_n,
        )
        return message