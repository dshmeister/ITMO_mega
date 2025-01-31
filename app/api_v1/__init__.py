__all__ = ("router")
from .tickets import router as query_router
from ..core.auth.authorization import get_api_key
from fastapi import APIRouter, Depends

# Initializing ticket-router
#router = APIRouter(dependencies=[Depends(get_api_key)])


# Если нужен Bearer-token, то прокиньте его в окружение и поменяйте 7 и 11 строчки местами
router = APIRouter()

# Including ticket-router to default with tag TICKET
router.include_router(query_router, tags=["QUERY"])
