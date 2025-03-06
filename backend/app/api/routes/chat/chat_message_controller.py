import uuid
import asyncio
from typing import Any, Annotated

from fastapi import Depends, APIRouter

from .chat_message_service import ChatMessageService
from app.core.services.reranking.reranking_cohere import RerankingCohereService



router = APIRouter(prefix="/chat_message", tags=["chat"])

def test_common_parameters():
    common_parameters = {
        "model": "rerank-v3.5",
        "query": "What is the capital of the United States?",
        "top_n": 3,
        "documents": [
            "Carson City is the capital city of the American state of Nevada.",
            "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",
            "Capitalization or capitalisation in English grammar is the use of a capital letter at the start of a word. English usage varies from capitalization in other languages.",
            "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.",
            "Capital punishment has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states.",
        ],
    }
    return common_parameters

 ### TO DO ###
# add a KB id to the router to be able to get a parameters for a agents (like Question Extractions)
# 

@router.get("/")
async def chat_message(
    params: Annotated[dict, Depends(test_common_parameters)],
    reranking_client: Annotated[Any, Depends(RerankingCohereService().start_session)],
) -> Any:
    """
    Chat message.
    """
    model = params["model"]
    top_n = params["top_n"]
    query = params["query"]
    documents = params["documents"]
    message = await ChatMessageService.create_message(
        reranking_client = reranking_client,
        model=model,
        top_n=top_n,
        query=query,
        documents=documents,
    )

    return message
