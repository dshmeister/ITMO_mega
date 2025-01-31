import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from .llm_config.prompts import PROMPT

class QuerySettings(BaseModel):
    LLM_HOST: str = os.getenv('LLM_HOST_URL')
    # Model Host for AtheneLLM model
    MODEL_NAME: str = os.getenv('MODEL_NAME')
    # API_KEY
    API_KEY: str = os.getenv('API_KEY')
    OPENROUTER_API_KEY: str = os.getenv('OPENROUTER_API_KEY')
    # Prompts
    PROMPT: str = PROMPT

    #model_config = SettingsConfigDict(env_file=DOTENV, extra="allow")


settings = QuerySettings()
