from fastapi import APIRouter, HTTPException, Depends
from ...core.config.logger import logger
from ...core.config.schemas import JSONOutput
from ...src.instance import get_search, get_llm
from ...src.utils import process_query
import json

# Initializing APIRouter
router = APIRouter()

# Default Endpoint for Ticket-Classification
@router.post("/api/request", response_model=JSONOutput)
async def ticket_response(
    input: str,
    id: int,
    llm = Depends(get_llm),
    search = Depends(get_search)
):
    try:
        logger.info(msg=f"Processing query: {input}")

        response_llm = await process_query(input, id)
        response_corrected = r"{}".format(response_llm)

        # Преобразуем в JSON
        response_data = json.loads(response_corrected)

        logger.info(msg='Processed SUCCESS.')


        return response_data

    except Exception as e:
        logger.error(f"Error processing ticket: {e}")
        raise HTTPException(status_code=500, detail="Error processing ticket")
