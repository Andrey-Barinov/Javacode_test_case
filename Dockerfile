FROM docker.io/library/python:3.10-slim

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000
# CMD ["sh", "-c", "poetry run python3 manage.py makemigrations && poetry run python3 manage.py migrate && poetry run python3 manage.py runserver 0.0.0.0:8000"]
CMD ["sh", "-c", "poetry run python3 manage.py wait_for_db && poetry run python3 manage.py makemigrations && poetry run python3 manage.py migrate && poetry run python3 manage.py runserver 0.0.0.0:8000"]

