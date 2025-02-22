from google import genai 
import asyncio
from typing import Optional, Union
from pydantic import BaseModel, Field

class ContentConfig(BaseModel):
    response_mime_type: str = 'text/plain'
    system_instruction: Optional[str] = None
    response_schema: Optional[dict] = None

    class Config:
        extra = 'forbid'  # Prevent extra fields in the configuration

    @classmethod
    def from_schema(
        cls,
        system_instruction: Optional[str] = None,
        response_schema: Optional[BaseModel] = None
        ):
        response_mime_type = 'application/json' if response_schema else 'text/plain'
        schema = response_schema.model_json_schema() if response_schema else None
        return cls(
            response_mime_type=response_mime_type,
            system_instruction=system_instruction,
            response_schema=schema
        )


class GeminiService:
    api_key = "AIzaSyDtbmHItBx-5-Ahb4YaAoAHuSYlDISOVcc"
    async def setup_client(self):
        client = genai.Client(api_key=self.api_key)
        return client

    async def generate_content(
        self,
        client: genai.Client,
        model: str,
        contents: Union[str, list],
        system_instruction: Optional[str] = None,
        response_schema: Optional[BaseModel] = None,
    ):
        """
        IF we use response_schema the function still returns response.text as str 
        """

        # Create a configuration object using the from_schema class method
        config = ContentConfig.from_schema(
            system_instruction=system_instruction,
            response_schema=response_schema
        )

        response = await client.aio.models.generate_content( #.aio is a method for asynchroniq interactions
            model=model,
            config=config.model_dump(exclude_none=True),  # Convert to dictionary, excluding None values
            contents=contents,
        )

        return response