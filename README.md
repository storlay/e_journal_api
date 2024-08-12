<h1 align="center">API: Электронный журнал для оценок 📒</h1>

<div align="center">

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-8B3E2F?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)](https://python-poetry.org/)


</div>

## Основные возможности

### 1. Оценки

- **GET `/api/v1/scores/all`**:
    - Получить список всех оценок (с пагинацией).

- **GET `/api/v1/scores/{id}`**:
    - Получить информацию об оценке по ID.

- **POST `/api/v1/scores/add`**:
    - Добавить новую оценку.

- **PUTCH `/api/v1/scores/{id}`**:
    - Обновить существующую оценку по ID.

- **DELETE `/api/v1/scores/{id}`**:
    - Удалить оценку по ID.

### 2. Ученики

- **GET `/api/v1/students/all`**:
    - Получить список всех ученикоы (с пагинацией).

- **GET `/api/v1/students/{id}`**:
    - Получить информацию об ученике по ID.

- **POST `/api/v1/students/add`**:
    - Добавить нового ученика.

- **PUTCH `/api/v1/students/{id}`**:
    - Обновить информацию о существующем ученике по ID.

- **DELETE `/api/v1/students/{id}`**:
    - Удалить ученика по ID.

## Установка и запуск

1. Склонируйте репозиторий:

```
git clone https://github.com/storlay/e_journal_api.git
```

2. В корне создайте и заполните файл `.env`


3. Запустите проект с помощью Docker Compose:

```
docker compose -f infra/docker-compose.dev.yml up --build
```

4. Приложение будет доступно по адресу http://127.0.0.1:8000

## Использование

- **Документация API** доступна по адресам:
    - http://127.0.0.1:8000/docs (Swagger)
    - http://127.0.0.1:8000/redoc (Redoc)