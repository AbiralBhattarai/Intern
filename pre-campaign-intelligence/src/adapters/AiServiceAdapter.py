from google import genai

from src.ports.output.AiServicePort import AiServicePort


class GeminiAiServiceAdapter(AiServicePort):
    """
    Adapter for Google Gemini AI service.
    Implements the AiServicePort interface.
    """

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        """
        Initialize the Gemini AI adapter with injected dependencies.
        
        Args:
            api_key: Google API key for authentication
            model: Model name to use (default: gemini-2.0-flash)
        """
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate content using the Gemini model.
        
        Args:
            system_prompt: System instruction/context
            user_prompt: User's prompt
            
        Returns:
            Generated response text
        """
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
        )

        return response.text