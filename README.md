# Javacode_test_case
[![Python CI](https://github.com/Andrey-Barinov/Javacode_test_case/actions/workflows/pyci.yml/badge.svg)](https://github.com/Andrey-Barinov/Javacode_test_case/actions/workflows/pyci.yml)
<a href="https://codeclimate.com/github/Andrey-Barinov/Javacode_test_case/test_coverage"><img src="https://api.codeclimate.com/v1/badges/a945bd894fc205206dfe/test_coverage" /></a>
---
Разработайте приложение, которое будет принимать и обрабатывать REST-запросы для управления кошельками. Приложение должно поддерживать следующие операции:

1. **Пополнение или снятие средств с кошелька:**

   - **Метод:** `POST`
   - **URL:** `/api/v1/wallets/<WALLET_UUID>/operation`
   - **Тело запроса:**
     ```json
     {
       "operationType": "DEPOSIT" or "WITHDRAW",
       "amount": 1000
     }
     ```

   После получения запроса необходимо выполнить логику изменения баланса кошелька в базе данных.

2. **Получение баланса кошелька:**

   - **Метод:** `GET`
   - **URL:** `/api/v1/wallets/<WALLET_UUID>`

**Стек технологий:**

- FastAPI / Flask / Django
- PostgreSQL

**Требования:**

- Написать миграции для базы данных с помощью Liquibase (по желанию).
- Обратить особое внимание на работу в конкурентной среде (1000 RPS на один кошелек). Ни один запрос не должен завершаться с ошибкой сервера (HTTP 50X).
- Обеспечить корректный формат ответа на заведомо неверные запросы, например, если кошелек не существует, JSON не валиден, или недостаточно средств на счете.
- Приложение и база данных должны запускаться в Docker-контейнерах. Вся система должна подниматься с помощью `docker-compose`.
- Предусмотреть возможность настройки различных параметров приложения и базы данных без пересборки контейнеров.
- Эндпоинты должны быть покрыты тестами.
- Решение необходимо разместить на GitHub и предоставить ссылку на репозиторий.
- Все возникающие вопросы по заданию решать самостоятельно.

  ---
  <b>Все задания выполнены кроме миграций с помощью Liquibase. Также добавленны эднпонты для создания кошелька и списка всех кошельков.</b>

## Стек:

```
python = "^3.10"
django = "^5.1"
djangorestframework = "^3.15.2"
psycopg2-binary = "^2.9.10"
python-dotenv = "^1.0.1"
dj-database-url = "^2.2.0"
django-wait-for-db = "^1.0.6"
```

## Установка:

**Docker-контейнер:**
cd Javacode_test_case/
1. Необходимо иметь установленный Docker и Docker compose
2. Клонировать репозиторий: **`git clone git@github.com:Andrey-Barinov/Javacode_test_case.git`**
3. Перейти в директорию:  **`cd Javacode_test_case/`**
4. Собрать Docker compose образ: **`docker compose build`**
5. Запустить сервер: **`docker compose up`**
6. Зайти в браузер и перейти по адресу **`http://localhost:8000`**

**Примечание:**
Нахождение файла .env в репозитории носит чисто ознакомительный характер. Файл .env и секретные данные не должны храниться в публичном доступе.
