from fastapi import FastAPI
from .api_v1 import router as api_v1_router
from .src.llm_engine import QwenRequestGPU6, OpenRouterRequest
from .src.search_engine import AsyncTavilySearch
from .core.config.base_model import settings
from .core.config.logger import logger
from .src.instance import set_search, set_llm
import uvicorn


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Инициализация RAG при запуске приложения"""
    try:
        # Initializing LLM-engine instance
        # qwen_request = QwenRequestGPU6(
        #     llm_host=settings.LLM_HOST,
        #     model_name=settings.MODEL_NAME,
        #     prompt=settings.PROMPT
        # )
        # set_llm(qwen_request)

        gemini_request = OpenRouterRequest(
            llm_host="https://openrouter.ai/api/v1",
            # model_name= "qwen/qwen-2.5-7b-instruct",
            model_name="anthropic/claude-3-haiku",
            prompt=settings.PROMPT
        )
        set_llm(gemini_request)
        logger.info(msg='LLM-Instance init OK.')

        # Initializing Search-engine instance
        search_engine = AsyncTavilySearch(api_key=settings.API_KEY)
        set_search(search_engine)
        logger.info(msg='Search-Instance init OK.')
    except Exception as e:
        logger.info(msg=f"Ошибка при инициализации RAG: {e}")
        raise


app.include_router(api_v1_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)