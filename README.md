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
  "query": "В каком году Университет ИТМО был включён в число Национальных исследовательских университетов России?\n1. 2007\n2. 2009\n3. 2011\n4. 2015",
  "id": 2
}
```
- **query** *(string)* — текст запроса с пронумерованными вариантами ответа.
- **id** *(integer)* — идентификатор запроса.

### 🔹 Выходные параметры
```json
{
  "id": 2,
  "answer": 2,
  "reasoning": "Университет ИТМО был включён в число Национальных исследовательских университетов России в 2009 году. Это подтверждается официальными данными Министерства образования и науки РФ.",
  "sources": [
    "https://www.itmo.ru",
    "https://минобрнауки.рф"
  ]
}
```
- **id** *(integer)* — идентификатор запроса.
- **answer** *(integer|null)* — номер правильного ответа (если применимо), иначе `null`.
- **reasoning** *(string)* — объяснение выбора ответа.
- **sources** *(list of strings)* — список источников информации.

## 🚀 Установка и запуск
### 1. ⚡ Локальный запуск
**Требования:**
- Python 3.10+
- Установленный `pip`
- Локально развернутый Qwen-14B

#### 🔧 Установка зависимостей
```bash
pip install -r requirements.txt
```

## 🔧 Настройка переменных окружения (.env)
Для работы сервиса необходимо создать файл `.env` и указать в нем следующие параметры:

```env
LLM_HOST_URL="http://localhost:4000/v1/chat/completions"  # URL развернутого LLM-сервера
MODEL_NAME="qwen-14b"  # Название используемой модели
API_KEY="your_tavily_api_key"  # API ключ для Tavily
BEARER_TOKEN="your_secret_token"  # Токен авторизации для API
```

Этот файл не должен быть загружен в репозиторий (добавьте его в `.gitignore`).

#### ▶ Запуск сервиса
```bash
python main.py
```

### 2. 🐳 Запуск с Docker
**Шаг 1:** Соберите образ Docker
```bash
docker build -t query_extraction .
```

**Шаг 2:** Запустите контейнер
```bash
docker-compose up -d
```

**API будет доступно по адресу:** `http://localhost:13001/api/request`


## 🚀 Запуск LLM с vLLM

### 🔹 Загрузка модели с Hugging Face
```bash
pip install vllm
huggingface-cli download Qwen/Qwen-14B --local-dir ./models/qwen-14b
```

### 🔹 Dockerfile для vLLM
Создайте `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN pip install vllm

COPY models/qwen-14b /models/qwen-14b

CMD ["python3", "-m", "vllm.entrypoints.api_server", "--model", "/models/qwen-14b"]
```

### 🔹 Запуск vLLM с Docker Compose
Создайте `docker-compose.yml`:
```yaml
version: '3.9'
services:
  vllm-server:
    build: .
    container_name: vllm_qwen
    volumes:
      - ./models/qwen-14b:/models/qwen-14b
    ports:
      - "4000:4000"
```
Запустите сервер:
```bash
docker-compose up -d
```

## 🌐 Настройка Nginx и DNS
### 🔹 Регистрация домена
Чтобы ваш сервис был доступен через доменное имя, вам нужно зарегистрировать домен у любого регистратора. После регистрации необходимо создать `A-запись`, указывающую на IP-адрес вашего сервера.

### 🔹 Конфигурация Nginx
Пример конфигурации Nginx (`/etc/nginx/sites-available/itmo_query`):
```nginx
server {
    listen 80;
    server_name itmo-query.example.com;

    location / {
        proxy_pass http://localhost:13001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
Активация:
```bash
ln -s /etc/nginx/sites-available/itmo_query /etc/nginx/sites-enabled/
systemctl restart nginx
```

## ✍ Автор
**Волосников Кирилл**, Jun+ MLOps

🎯 **Проект готов к использованию :)))) GL HF!** 🚀



