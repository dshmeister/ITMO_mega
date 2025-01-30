import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LLM_HOST = os.getenv('LLM_HOST_URL')
MODEL_NAME = os.getenv('MODEL_NAME')
API_KEY = os.getenv('API_KEY')