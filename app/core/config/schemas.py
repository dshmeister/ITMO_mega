from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class JSONOutput(BaseModel):
    id: int  # Числовой идентификатор запроса
    answer: Optional[int]  # Числовой ответ, если применимо, иначе None
    reasoning: str  # Объяснение или дополнительная информация
    sources: List[HttpUrl]  # Список ссылок на источники (если есть, иначе пустой список)