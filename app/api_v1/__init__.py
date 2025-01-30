__all__ = ("router")
from .tickets import router as query_router
from ..core.auth.authorization import get_api_key
from fastapi import APIRouter, Depends

# Initializing ticket-router
router = APIRouter(dependencies=[Depends(get_api_key)])

# Including ticket-router to default with tag TICKET
router.include_router(query_router, tags=["QUERY"])
