import asyncio
import logging
from aiohttp.web_exceptions import HTTPBadRequest
from tavily import AsyncTavilyClient
from ..core.config.logger import logger
from ..core.config.base_model import settings

class AsyncTavilySearch:
    def __init__(self, api_key: str):
        """
        Инициализация AsyncTavilySearch.

        :param api_key: API ключ для Tavily.
        """
        self.tavily_client = AsyncTavilyClient(api_key=settings.API_KEY)  # Используем Async-клиент

    async def search(self, query: str) -> dict:
        """
        Выполнение асинхронного поискового запроса к Tavily API.

        :param query: Поисковый запрос.
        :return: Ответ от API в формате JSON.
        """
        try:
            response = await self.tavily_client.search(query)  # Асинхронный вызов
            logger.info(f"Search query '{query}' completed successfully.")
            return response
        except Exception as e:
            logger.error(f"Error executing search query '{query}': {e}")
            raise HTTPBadRequest(text=f"Error executing search query: {e}")

    async def format_search_results(self, response: dict) -> str:
        """
        Форматирование результатов поиска в строку.

        :param response: Ответ от API Tavily.
        :return: Строка с отформатированными результатами.
        """
        try:
            text = ''
            for result in response.get("results", []):
                text += f'____URL: {result.get("url", "N/A")} Title: {result.get("title", "No title")} Content: {result.get("content", "No content")}\n'
            logger.info("Search results formatted successfully.")
            return text.strip()
        except KeyError as e:
            logger.error(f"Key error in search results: {e}")
            raise HTTPBadRequest(text=f"Key error in search results: {e}")
        except Exception as e:
            logger.error(f"Error formatting search results: {e}")
            raise HTTPBadRequest(text=f"Error formatting search results: {e}")

    async def tavily_request(self, query: str) -> str:
        """
        Выполнение поискового запроса и форматирование результатов.

        :param query: Поисковый запрос.
        :return: Строка с отформатированными результатами.
        """
        try:
            response = await self.search(query)  # Делаем поиск
            return await self.format_search_results(response)  # Форматируем результаты
        except Exception as e:
            logger.error(f"Error in tavily_request for query '{query}': {e}")
            raise HTTPBadRequest(text=f"Error in tavily_request: {e}")
