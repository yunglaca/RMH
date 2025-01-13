
test task

# RMH

CRUD + tests + docker

## Как запустить локально (нужен python 3.12 + postgresql)


Заполнить .env файл по примеру .env.example.

pip install requirements.txt


uvicorn main:app --reload

Либо через докер:

```bash
docker-compose up --build
docker-compose up
```
