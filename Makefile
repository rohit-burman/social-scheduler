SHELL := /bin/bash

.PHONY: deps up down web api worker scheduler monitor lint test

deps:
	pnpm install
	cd apps/api && uv sync --extra celery

up:
	docker compose -f infra/docker/docker-compose.yml up -d

down:
	docker compose -f infra/docker/docker-compose.yml down

web:
	pnpm --filter web dev

api:
	cd apps/api && uv run uvicorn src.main:app --reload --port 8000

worker:
	cd apps/api && uv run celery -A src.config.celery worker --loglevel=info -Q publish,default

scheduler:
	cd apps/api && uv run celery -A src.config.celery beat --loglevel=info

monitor:
	cd apps/api && uv run celery -A src.config.celery flower

lint:
	pnpm lint
	cd apps/api && uv run ruff check .

test:
	pnpm test
	cd apps/api && uv run pytest
