# ITMO Query Extraction API

## 📌 Описание
Этот сервис — интеллектуальный бот для обработки запросов, связанных с Университетом ИТМО. Он сочетает в себе поисковый движок Tavily и мощную языковую модель Qwen-14B (запущенную локально на выделенном сервере) для предоставления точных и актуальных ответов.

### 🔥 Ключевые возможности
- **Поиск актуальной информации**: Использует Tavily API для извлечения свежих данных из Интернета.
- **Мощный LLM-агент**: Интеграция с локально развернутым Qwen-14B для формирования ответов на естественном языке.
- **REST API**: Поддержка FastAPI для быстрого и удобного взаимодействия.
- **Docker-контейнеризация**: Простая развертка с использованием `Docker` и `docker-compose`.
- **CI/CD**: В данном проекте CI/CD пока не используется, но разработан GitLab CI/CD пайплайн, который можно интегрировать при необходимости (требуется GitLab Runner).

## 🏗 Архитектура проекта

📂 **Структура проекта**
```
ITMO_mega/
│── app/
│   ├── api_v1/
│   │   ├── tickets/
│   │   │   ├── views.py  # Основной обработчик API
│   │── core/
│   │   ├── auth/
│   │   │   ├── authorization.py  # Авторизация и проверка токена
│   │   ├── config/
│   │   │   ├── llm_config/
│   │   │   │   ├── prompts.py  # Шаблоны промптов
│   │   │   ├── base_model.py  # Настройки базовой модели
│   │   │   ├── logger.py  # Логирование событий
│   │   │   ├── schemas.py  # Описание схем API
│   ├── src/
│   │   ├── instance.py  # Управление экземплярами LLM и поисковика
│   │   ├── llm_engine.py  # Взаимодействие с Qwen-14B
│   │   ├── search_engine.py  # Интеграция с Tavily API
│   │   ├── utils.py  # Вспомогательные утилиты
│── main.py  # Точка входа
│── .env  # Конфигурационные переменные
│── docker-compose.yml
│── Dockerfile
│── .gitlab-ci.yml  # CI/CD конфигурация (не используется в текущей версии)
│── README.md
```

## 📥 Входные и выходные данные

### 🔹 Входные параметры (POST `/api/request`)
```json
{
  "query": "Текст запроса с вариантами ответа",
  "id": 1
}
```
- **query** *(string)* — вопрос пользователя, который включает нумерованные варианты ответа.
- **id** *(integer)* — идентификатор запроса.

### 🔹 Выходные параметры
```json
{
  "id": 1,
  "answer": 2,
  "reasoning": "Обоснование ответа, предоставленного моделью.",
  "sources": [
    "https://example.com/source1",
    "https://example.com/source2"
  ]
}
```
- **id** *(integer)* — идентификатор запроса.
- **answer** *(integer|null)* — номер правильного ответа (если применимо), иначе `null`.
- **reasoning** *(string)* — объяснение, почему выбран этот ответ.
- **sources** *(list of strings)* — список источников информации.

## ⚙ Настройка переменных окружения
Создайте файл `.env` и добавьте следующие параметры:
```env
LLM_HOST_URL="http://localhost:4000/v1/chat/completions"
MODEL_NAME="qwen-14b"
API_KEY="your_tavily_api_key"
BEARER_TOKEN="your_secret_token"
```

## 🛠 Используемые технологии
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tavily API](https://www.tavily.com/)
- [Qwen-14B](https://github.com/QwenLM)
- [Docker](https://www.docker.com/)
- [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)
- [Gunicorn](https://gunicorn.org/) + Uvicorn
- [Logging](https://docs.python.org/3/library/logging.html)
- [Asyncio](https://docs.python.org/3/library/asyncio.html)
- [Pydantic](https://pydantic-docs.helpmanual.io/) — валидация данных
- [Aiohttp](https://docs.aiohttp.org/) — асинхронные HTTP-запросы
- [Pytest](https://docs.pytest.org/) — тестирование

## 🚀 CI/CD
В текущей версии проекта **CI/CD не используется**, но подготовлен GitLab CI/CD скрипт, который можно задействовать при необходимости (требуется GitLab Runner).

## ✍ Автор
**Волосников Кирилл**, Jun+ MLOps

🎯 **Готов к использованию!** 🚀

