from app.core.config import settings
from google import genai
from app.core.dtos.generative_models import GeminiGenerationInstruction

class GeminiService:
    @staticmethod
    async def setup_client() -> genai.Client:
        return genai.Client(api_key=settings.GOOGLE_GEMINI_API_KEY)

    @staticmethod
    async def generate_content(
        params: GeminiGenerationInstruction,
    ) -> genai.types.GenerateContentResponse:
        """
        Generate content using the Gemini AI model.

        Args:
            client (genai.Client): The client to use for the request.
            params (GenerateContentInstruction): The parameters to pass to the model.

        Returns:
            genai.Response: The response returned by the model.
        """
        response = await params.client.aio.models.generate_content(**params.build_parameters())

        return response
    
    @staticmethod
    async def get_text_response(response: genai.types.GenerateContentResponse) -> str:
        """
        Extract the text response from the Gemini AI response.

        Args:
            response (genai.types.GenerateContentResponse): The response from the Gemini AI model.

        Returns:
            str: The text response from the Gemini AI model.
        """
        return response.text
    
setup_client = GeminiService.setup_client

