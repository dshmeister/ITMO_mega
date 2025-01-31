import asyncio
from ..core.config.logger import logger
from .instance import get_llm, get_search
import json
import re


async def process_query(query: str, id: int):
    """
    Асинхронная обработка запроса от пользователя

    :param query: Запрос пользователя.
    :return: Ответ от модели.
    """
    llm = get_llm()
    search = get_search()
    try:
        search_results = await search.tavily_request(query)
        qwen_response = await llm.get_response_content(search_results, query, id)

        # Returning LLM response
        return qwen_response
    except Exception as e:
        logger.info(msg=f"")
        raise



def extract_json(text):
    """
    Извлекает JSON из текста, удаляя лишние символы.
    """
    try:
        # Ищем первую "{" и последнюю "}"
        json_start = text.find("{")
        json_end = text.rfind("}") + 1

        if json_start == -1 or json_end == -1:
            raise ValueError("Не найден корректный JSON-ответ.")

        json_text = text[json_start:json_end]

        # Убираем переносы строк, возможные кавычки и управляющие символы
        json_text = re.sub(r'[\x00-\x1F\x7F]', '', json_text)

        return json.loads(json_text)  # Преобразуем в JSON
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON: {str(e)}")
        return {"error": "Ошибка обработки JSON", "raw_response": text}
    except Exception as e:
        logger.error(f"Не удалось извлечь JSON: {str(e)}")
        return {"error": "Ошибка извлечения JSON", "raw_response": text}



