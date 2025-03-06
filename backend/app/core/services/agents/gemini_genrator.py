from app.core.dtos.generative_models import GeneralGenerateInstruction
from pydantic import BaseModel, Field
from enum import Enum, auto
from typing import Optional,Type
from app.core.dtos.agents import Agents
from app.core.services.agents.agent_abstraction import Agent, InvokeParameters, AgentResponse
from google import genai 
from app.core.config import settings


class GeminiAgent(Agent):
    def setup_client() -> genai.Client:
        client = genai.Client(api_key=settings.GOOGLE_GEMINI_API_KEY)
        return client

    async def invoke(invoke_parameters: InvokeParameters) -> genai.Response:
        response = await invoke_parameters.client.aio.models.generate_content(
            **invoke_parameters.client_parameters(),
        )

        return response


class GeminiAgentPipline():
    pass



class GeminiGenerationInstruction(GeneralGenerateInstruction):
    """Parameters to generate content using Gemini AI model"""
    agent: Agents
    client: object = None
    response_mime_type: Optional[str] = None

    def __init__(self, **kwargs):
        from app.core.services.ai.gemini import setup_client
        
        kwargs['client'] = setup_client()
        response_schema = kwargs.get('response_schema')
        if response_schema:
            kwargs['response_mime_type'] = 'application/json'
            kwargs['response_schema'] = response_schema
        else:
            kwargs['response_mime_type'] = 'text/plain'
        super().__init__(**kwargs)

    def build_parameters(self):
        """Build parameters for the Gemini generate endpoint"""
        return {
            "model": self.model,
            "config": {
                "system_instruction": self.system_instruction,
                "response_schema": self.response_schema if self.response_schema else None,
                "response_mime_type": self.response_mime_type
            },
            "contents": self.user_input
        }

class ResponseMineType(str, Enum):
    PLAIN = 'text/plain'
    JSON = 'application/json'

class GeminiConfig(BaseModel):
    system_instruction: str
    response_schema: str
    response_mime_type: ResponseMineType


class GeminiInvokeSchema(BaseModel):
    """
    Parameters to invoke a Gemini AI model.
    Full model is:
        model: str
        config:
            system_instruction: str
            response_schema: str
            response_mime_type:
                PLAIN
                JSON
        contents: str
    """
    model: str
    config: GeminiConfig
    contents: str


class GeminiNotUserSettings(BaseModel):
    model: Optional[str] = None
    system_instruction: Optional[str] = None
    response_schema: Optional[Type[BaseModel]] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class GeminiUserSettings():
    pass


class _GeminiAgent():
    @staticmethod
    def setup_client ():
        pass

    @staticmethod
    def invoke(invoke_parameters: InvokeParameters) -> AgentResponse:
        pass


    def map_no_user_settings_to_invoke_parameters(
        self, 
        no_user_settings: GeminiNotUserSettings
    ) -> GeminiInvokeSchema:
        pass