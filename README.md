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

