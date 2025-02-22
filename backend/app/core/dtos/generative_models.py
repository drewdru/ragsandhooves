from typing import Optional,Type
from pydantic import BaseModel, Field
from app.core.models.agents_parameters import Agents

class GeneralGenerateInstruction(BaseModel):
    agent: Optional[str] = None
    client: Optional[object] = None
    model: Optional[str] = None
    system_instruction: Optional[str] = None
    user_input: Optional[str] = None
    response_schema: Optional[Type[BaseModel]] = None

    def get_kb_parameters(
        self, 
        knowledge_base_id: Optional[str] = None
    ):
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


if __name__ == "__main__":
    print ("Hello World")