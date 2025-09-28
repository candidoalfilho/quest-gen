from pydantic import BaseModel

class ConfigClass(BaseModel):
    LLM_MODEL: str
    GEMINI_API_KEY: str