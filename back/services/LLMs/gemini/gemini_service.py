from services.LLMs.base_llm_service import BaseLLM
from instructor import from_gemini
from google.generativeai import configure, GenerativeModel
from google.generativeai.types import GenerationConfig

from core.config import env_config
from services.LLMs.gemini.retry import retry_strategy
from pydantic import BaseModel

class GeminiLLM(BaseLLM):

    def __init__(self):
        gemini_model = self._configure_client()
        self.client = from_gemini(client=gemini_model)

    def _configure_client(self):
        configure(api_key=env_config.GEMINI_API_KEY)
        gemini_model = GenerativeModel(
            model_name=env_config.LLM_MODEL,
            generation_config=GenerationConfig(
                temperature=0.3,
                top_p=0.7,
            )
        )

        return gemini_model

    @retry_strategy
    def generate_response(self, system_prompt: str, user_prompt: str, response_schema: BaseModel):
        try:
            response = self.client.messages.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    },
                ],
                response_model=response_schema   
            )

            return response
        
        except Exception as e:
            raise e