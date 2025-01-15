
test task

# RMH

CRUD + tests + docker

## Как запустить локально (нужен python 3.12 + postgresql)


Заполнить .env файл по примеру .env.example.


создать venv


pip install requirements.txt


uvicorn main:app --reload

### Либо через докер:

```bash
Заполнить .env файл по примеру .env.example.
docker-compose up --build
```

#### Тестирование через pytest

```bash
pytest
```
