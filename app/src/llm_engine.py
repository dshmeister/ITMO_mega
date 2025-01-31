import asyncio
import logging
from aiohttp import ClientSession, ClientResponseError
from aiohttp.web_exceptions import HTTPBadRequest
from tavily import TavilyClient
from ..core.config.logger import logger
from ..core.config.base_model import settings
from openai import OpenAI
import re

class QwenRequestGPU6:
    def __init__(self, llm_host: str, model_name: str, prompt: str):
        """
        Инициализация класса QwenRequestGPU6.

        :param llm_host: URL сервера с моделью.
        :param model_name: Название модели.
        :param prompt: Промпт, который будет добавляться к запросу.
        """
        self.llm_host = llm_host
        self.model_name = model_name
        self.prompt = prompt

    async def _prepare_payload(self, search_results: str, query: str, id: int) -> dict:
        """
        Подготовка payload для запроса.

        :param search_results: Результаты поиска.
        :param query: Запрос клиента.
        :param id: id запроса.
        :return: Словарь с payload.
        """
        try:
            payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"{self.prompt}{search_results}Запрос клиента{query} ID: {id}"
                            }
                        ]
                    }
                ]
            }
            logger.info("Payload prepared successfully.")
            return payload
        except Exception as e:
            logger.error(f"Error preparing payload: {e}")
            raise HTTPBadRequest(text=f"Error preparing payload: {e}")

    async def _send_request(self, payload: dict) -> dict:
        """
        Отправка асинхронного запроса на сервер.

        :param payload: Данные для отправки.
        :return: Ответ от сервера в формате JSON.
        """
        try:
            headers = {"Content-Type": "application/json"}
            async with ClientSession() as session:
                async with session.post(self.llm_host, headers=headers, json=payload) as response:
                    response.raise_for_status()
                    logger.info("Request to LLM server completed successfully.")
                    return await response.json()
        except ClientResponseError as e:
            logger.error(f"HTTP error sending request to LLM server: {e.status} - {e.message}")
            raise HTTPBadRequest(text=f"HTTP error sending request to LLM server: {e.status} - {e.message}")
        except Exception as e:
            logger.error(f"Error sending request to LLM server: {e}")
            raise HTTPBadRequest(text=f"Error sending request to LLM server: {e}")

    async def get_response_content(self, search_results: str, query: str, id: int) -> str:
        """
        Асинхронное получение содержания ответа от модели.

        :param search_results: Результаты поиска.
        :param query: Запрос клиента.
        :param id: id запроса
        :return: Текст ответа от модели.
        """
        try:
            payload = await self._prepare_payload(search_results, query, id)
            response_json = await self._send_request(payload)
            logger.info("Response content retrieved successfully.")
            return response_json['choices'][0]['message']['content']
        except KeyError as e:
            logger.error(f"Key error in response JSON: {e}")
            raise HTTPBadRequest(text=f"Key error in response JSON: {e}")
        except Exception as e:
            logger.error(f"Error getting response content: {e}")
            raise HTTPBadRequest(text=f"Error getting response content: {e}")

class OpenRouterRequest:
    def __init__(self, llm_host: str, model_name: str, prompt: str):
        """
        Инициализация класса OpenRouterRequest.

        :param llm_host: URL OpenRouter API.
        :param model_name: Название модели (например, "google/gemini-flash-1.5-8b").
        :param prompt: Промпт, который будет добавляться к запросу.
        """
        self.llm_host = llm_host
        self.model_name = model_name
        self.prompt = prompt
        self.client = OpenAI(base_url=self.llm_host, api_key=settings.OPENROUTER_API_KEY)

    async def _prepare_payload(self, search_results: str, query: str, id: int) -> dict:
        """
        Подготовка payload для запроса.

        :param search_results: Результаты поиска.
        :param query: Запрос клиента.
        :param id: id запроса.
        :return: Словарь с payload.
        """
        try:
            payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"{self.prompt}{search_results} Запрос клиента: {query} ID: {id}"}
                        ]
                    }
                ]
            }
            logger.info("Payload prepared successfully.")
            return payload
        except Exception as e:
            logger.error(f"Error preparing payload: {e}")
            raise HTTPBadRequest(text=f"Error preparing payload: {e}")

    async def _send_request(self, payload: dict):
        """
        Отправка асинхронного запроса на сервер.

        :param payload: Данные для отправки.
        :return: Объект OpenRouter API (ChatCompletion).
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=payload["messages"]
            )
            logger.info("Request to LLM server completed successfully.")

            return completion  # Возвращаем **объект**, а не словарь
        except Exception as e:
            logger.error(f"Error sending request to LLM server: {e}")
            raise HTTPBadRequest(text=f"Error sending request to LLM server: {e}")

    async def get_response_content(self, search_results: str, query: str, id: int) -> str:
        """
        Асинхронное получение содержания ответа от модели.

        :param search_results: Результаты поиска.
        :param query: Запрос клиента.
        :param id: id запроса.
        :return: Текст ответа от модели.
        """
        try:
            payload = await self._prepare_payload(search_results, query, id)
            response = await self._send_request(payload)

            # **Правильный способ извлечь текст**
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                logger.info("Response content retrieved successfully.")
                return content

            raise KeyError("Response does not contain valid 'choices[0].message.content'")
        except KeyError as e:
            logger.error(f"Key error in response: {e}. Full response: {response}")
            raise HTTPBadRequest(text=f"Key error in response: {e}")
        except Exception as e:
            logger.error(f"Error getting response content: {e}. Full response: {response}")
            raise HTTPBadRequest(text=f"Error getting response content: {e}")