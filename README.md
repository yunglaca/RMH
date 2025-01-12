# RMH
test task

# RMH

CRUD + tests + docker

## Как запустить локально (нужен python 3.12 + postgresql)


Заполнить .env файл по примеру .env.example.
uvicorn main:app --reload

Через докер:

```bash
docker-compose up --build
docker-compose up
```