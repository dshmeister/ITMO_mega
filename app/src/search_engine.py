import asyncio
import logging
from aiohttp import ClientSession, ClientResponseError
from aiohttp.web_exceptions import HTTPBadRequest
from tavily import TavilyClient
from ..core.config.logger import logger
from ..core.config.base_model import settings

class AsyncTavilySearch:
    def __init__(self, api_key: str):
        """
        Инициализация AsyncTavilySearch.

        :param api_key: API ключ для Tavily.
        """
        self.tavily_client = TavilyClient(api_key=settings.API_KEY)

    async def search(self, query: str) -> dict:
        """
        Выполнение асинхронного поискового запроса к Tavily API.

        :param query: Поисковый запрос.
        :return: Ответ от API в формате JSON.
        """
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.tavily_client.search, query)
            logger.info(f"Search query '{query}' completed successfully.")
            print(response)
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
            for result in response['results']:
                text += f'____URL: {result["url"]} Title: {result["title"]} Content: {result["content"]}'
            logger.info("Search results formatted successfully.")
            return text
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
            response = await self.search(query)
            return await self.format_search_results(response)
        except Exception as e:
            logger.error(f"Error in tavily_request for query '{query}': {e}")
            raise HTTPBadRequest(text=f"Error in tavily_request: {e}")