#!/bin/bash

alembic revision --autogenerate
alembic upgrade head
if [[ "${1}" == "dev" ]]; then
    gunicorn src.main:app --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
elif [[ "${1}" == "test" ]]; then
    gunicorn src.main:app --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8080
fi