from fastapi import APIRouter, HTTPException, Depends
from ...core.config.logger import logger
from ...core.config.schemas import JSONOutput
from ...src.instance import get_search, get_llm
from ...src.utils import process_query, extract_json
import json

# Initializing APIRouter
router = APIRouter()

# Default Endpoint for Query Answers
@router.post("/api/request", response_model=JSONOutput)
async def query_response(
    query: str,
    id: int,
    llm = Depends(get_llm),
    search = Depends(get_search)
):
    try:
        logger.info(msg=f"Processing query: {query}")

        response_llm = await process_query(query, id)

        logger.info(msg=f"RESPONSE_LLM: {response_llm}")

        # Преобразуем ответ в JSON
        response_data = extract_json(response_llm)

        # Проверяем, что JSON корректный
        if "error" in response_data:
            raise ValueError(response_data["error"])

        logger.info(msg='Processed SUCCESS.')
        return response_data

    except Exception as e:
        logger.error(f"Error processing ticket: {e}")
        raise HTTPException(status_code=500, detail="Error processing ticket")
