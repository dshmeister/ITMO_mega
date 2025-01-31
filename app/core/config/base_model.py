import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from .llm_config.prompts import PROMPT


LLM_HOST = os.getenv('LLM_HOST_URL')
MODEL_NAME = os.getenv('MODEL_NAME')
API_KEY = os.getenv('API_KEY')


class QuerySettings(BaseModel):
    LLM_HOST: str = os.getenv('LLM_HOST_URL')
    # Model Host for AtheneLLM model
    MODEL_NAME: str = os.getenv('MODEL_NAME')
    # API_KEY
    API_KEY: str = os.getenv('API_KEY')
    # Prompts
    PROMPT: str = PROMPT

    #model_config = SettingsConfigDict(env_file=DOTENV, extra="allow")


settings = QuerySettings()


# import os
# from os.path import join, dirname
# from dotenv import load_dotenv
#
# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)
#
# LLM_HOST = os.getenv('LLM_HOST_URL')
# MODEL_NAME = os.getenv('MODEL_NAME')
# API_KEY = os.getenv('API_KEY')