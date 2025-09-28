import os
from dotenv import load_dotenv

from schemas.config_schema import ConfigClass

load_dotenv()

env_config = ConfigClass(
    GEMINI_API_KEY=os.getenv('GEMINI_API_KEY'),
    LLM_MODEL=os.getenv('LLM_MODEL')
)