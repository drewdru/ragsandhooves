import cohere
import asyncio
from app.core.config import settings

class RerankingCohereService:
    def start_session(self,):
        session = cohere.AsyncClientV2(
            api_key=settings.COHERE_API_KEY,
        )

        return session

    async def _get_documents_weights(
        self, reranker, model, query, documents, top_n
        ):
        """"
        Use Cohere Rerank API to get the weights of the documents.
        High weights shows that the document is more relevant to the query.

        Returns:
            Cohere Response Object. 
        """
        task = await reranker.rerank(
            model=model, 
            query=query, 
            documents=documents, 
            top_n=top_n
        )

        return task


    async def _rerank_original_documents(
        self, cohere_response, original_documents
        ):
        reranked_documents = []
        for i in cohere_response.results:
            reranked_documents.append(original_documents[i.index])

        return reranked_documents


    async def rerank_documents(
        self, reranker, model, query, documents, top_n,
        ):
        """"
        Take a list of documents and returns an ordered list of documents. 
        Documens are ordered by their relevance to the provided query from highest to lowest.
        Use top_n to specify the number of results to return.

        """
        cohere_response = await self._get_documents_weights(
            reranker, model, query, documents, top_n
        )

        reranked_documents = await self._rerank_original_documents(
            cohere_response, documents
        )

        return reranked_documents

    

