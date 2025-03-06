from google import genai 
from app.core.config import settings
from app.core.dtos.generative_models import GeminiGenerationInstruction

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import TypeVar,Any, Dict
from dataclasses import dataclass


class GeminiService:
    def setup_client():
        client = genai.Client(api_key=settings.GOOGLE_GEMINI_API_KEY)
        return client
    
    async def generate_content(
        params: GeminiGenerationInstruction,
    ):
        response = await params.client.aio.models.generate_content( #.aio is a method for asynchroniq interactions
            **params.build_parameters(),
        )

        return response
    
