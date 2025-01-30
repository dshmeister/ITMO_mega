import asyncio
from ..core.config.logger import logger
from .instance import get_llm, get_search


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







# from tavily import TavilyClient
# import requests
# import json
# import os
# from settings import API_KEY, MODEL_NAME, LLM_HOST
# from prompts import PROMPT
#
#
#
# # Step 1. Instantiating your TavilyClient
# tavily_client = TavilyClient(api_key=API_KEY)
#
#
# def qwen_request_gpu6(search_results, query):
#     url = LLM_HOST
#     headers = {
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model": MODEL_NAME,
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": str(PROMPT) + search_results + 'Запрос клиента' + query
#                     }
#                 ]
#             }
#         ]
#     }
#
#
#     response = requests.post(url, headers=headers, json=payload)
#     response_json = response.json()
#
#     content = response_json['choices'][0]['message']['content']
#
#     return content
#
#
# def tavily_request(prompt):
#     text = ''
#
#     # Step 2. Executing a simple search query
#     response = tavily_client.search(prompt)
#
#     print(response)
#     # Step 3. That's it! You've done a Tavily Search!
#     for result in response['results']:
#         #print('_' * 100)
#         #print(result['title'])
#         #print(result['content'])
#
#         text += '____URL:' + result['url'] +  'Title: ' + result['title'] + ' Content:' + result['content']
#
#     return text
#
# # 2
# query = """
# В каком городе находится главный кампус Университета ИТМО?\n1. Москва\n2. Санкт-Петербург\n3. Екатеринбург\n4. Нижний Новгород
# """
# # 2
# query_2 = """
# В каком году Университет ИТМО был включён в число Национальных исследовательских университетов России?\n1. 2007\n2. 2009\n3. 2011\n4. 2015
# """
# # 3
# query_3 = """
# В каком рейтинге (по состоянию на 2021 год) ИТМО впервые вошёл в топ-400 мировых университетов?\n1. ARWU (Shanghai Ranking)\n2. Times Higher Education (THE) World University Rankings\n3. QS World University Rankings\n4. U.S. News & World Report Best Global Universities
# """
#
# query_4 = """
# Как поступить в ai talent hub?
# """
# query_5 = """
# В каком году Университет ИТМО был включён в число Национальных исследовательских университетов России?\n1. 2007\n2. 2009\n3. 2011\n4. 2015
# """
#
# # Как выиграть в JMLC? ai talent hub
#
# query_6 = """
# Что такое мегашкола
# """
# print('*_' * 100)
# text = tavily_request(query_6)
# #print(text)
# qwen_response = qwen_request_gpu6(text, query_6)
# print(qwen_response)