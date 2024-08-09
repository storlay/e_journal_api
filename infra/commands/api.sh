#!/bin/bash

alembic revision --autogenerate
alembic upgrade head
gunicorn src.main:app --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000