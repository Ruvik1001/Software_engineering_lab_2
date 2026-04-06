# Лабораторная работа 2: Микросервисная REST API система

## Вариант

**Вариант 10: Планирование задач**

## Реализованные сервисы

- `proxy_service` - единая точка входа
- `auth_service` - JWT аутентификация
- `user_service` - пользователи (исполнители)
- `goal_service` - цели
- `task_service` - задачи
- `notification_service` - mock сервис (TODO для расширения)
- `calendar_service` - mock сервис (TODO для расширения)

## Структура проекта

```text
Software_engineering_lab_2/
├─ backend/
│  ├─ auth_service/
│  ├─ user_service/
│  ├─ goal_service/
│  ├─ task_service/
│  ├─ notification_service/
│  └─ calendar_service/
├─ wheelhouse_linux/         # колёса для офлайн-сборки (linux/amd64, cp312)
├─ wheelhouse_requirements.txt  # объединённый список версий для sync_wheelhouse
├─ scripts/
│  ├─ lint.ps1               # pylint/prospector по сервисам
│  ├─ sync_wheelhouse.ps1    # скачать колёса (Windows)
│  └─ sync_wheelhouse.sh     # скачать колёса (Linux/macOS)
├─ docker-compose.yml
├─ .pylintrc
└─ .prospector.yaml
```

Каждый сервис в `backend/*_service` имеет похожую внутреннюю структуру:

- `main.py` - точка входа FastAPI
- `api/` - HTTP endpoint'ы
- `schema/` - DTO для request/response
- `model/` - доменные модели
- `use_case/` - бизнес-логика
- `implementation/` - in-memory реализация репозиториев
- `interface/` - контракты (Protocol)
- `util/` - конфигурация и dependency providers
- `test/` - тесты сервиса

## Хранилище

Все сервисы используют in-memory хранилище в рамках контейнера.

## Запуск

Зависимости **зафиксированы по версиям** в `backend/*/requirements.txt` и в корневом `wheelhouse_requirements.txt`. В каталоге `wheelhouse_linux/` лежат готовые wheels для офлайн-сборки: при `docker compose build` pip **не ходит в PyPI** (`--no-index --find-links /wheels`).

В `docker-compose.yml` для всех сервисов задано `platform: linux/amd64`, чтобы один и тот же набор manylinux-колёс подходил на любой машине с Docker (включая Apple Silicon: контейнеры собираются под amd64).

```bash
docker compose up --build
```

Прокси: `http://localhost:8000`, Swagger: `http://localhost:8000/docs`.

### Обновить колёса (есть интернет)

Если вы меняете версии пакетов, сначала обновите `wheelhouse_requirements.txt` и зеркально `backend/*/requirements.txt`, затем:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\sync_wheelhouse.ps1
```

или на Linux/macOS: `chmod +x scripts/sync_wheelhouse.sh && ./scripts/sync_wheelhouse.sh`

После этого закоммитьте изменения в `wheelhouse_linux/`, чтобы клон репозитория снова собирался офлайн.

## Кодстайл и качество кода

В проекте используются:

- `pylint` (конфиг: `.pylintrc`)
- `prospector` (конфиг: `.prospector.yaml`)

Принятые правила:

- максимальная длина строки: `120`
- проверки запускаются по каждому сервису изолированно (чтобы не было конфликтов одноимённых пакетов `api`, `schema`, `util`)
- целевая оценка `pylint`: `9.9+` 

## Запуск линтера

### Windows / PowerShell (рекомендуется)

Из корня проекта:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\lint.ps1
```

Скрипт:

- запускает `pylint` для каждого `backend/*_service`
- затем запускает `prospector` для каждого `backend/*_service`

### Ручной запуск для одного сервиса

Пример для `auth_service`:

```powershell
$env:PYTHONPATH = (Resolve-Path .\backend\auth_service)
python -m pylint .\backend\auth_service --rcfile .\.pylintrc --score y
prospector .\backend\auth_service -o text --profile-path .
```

### Если сборка падает на офлайн-установке

При `--no-index` в образ попадают только файлы из `wheelhouse_linux/`. Типичные причины: каталог пустой после клона (нужен `git pull` с колёсами), либо меняли версии без повторного `sync_wheelhouse`. Скрипт `pip download` по `wheelhouse_requirements.txt` подтягивает и **транзитивные** зависимости (в том числе `pydantic_core` и др. нативные колёса под cp312/manylinux).

## Основные endpoint'ы через proxy

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/users`
- `GET /api/v1/users/by-login/{login}`
- `GET /api/v1/users/search?mask=...`
- `POST /api/v1/goals`
- `GET /api/v1/goals`
- `POST /api/v1/tasks`
- `GET /api/v1/tasks/by-goal/{goal_id}`
- `PATCH /api/v1/tasks/{task_id}/status`

## Тесты

```bash
pytest --cov=backend --cov-report=term-missing --cov-report=xml
```

## Примеры запросов и ответов

Базовый URL прокси: `http://localhost:8000`.

### Создание нового пользователя (регистрация)

Запрос:

```bash
curl -s -X POST "http://localhost:8000/api/v1/auth/register" ^
  -H "Content-Type: application/json" ^
  -d "{\"login\":\"john@example.com\",\"password\":\"qwerty\",\"first_name\":\"John\",\"last_name\":\"Doe\"}"
```

Ответ (200):

```json
{
  "user_id": 1,
  "login": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Логин (получение JWT)

Запрос:

```bash
curl -s -X POST "http://localhost:8000/api/v1/auth/login" ^
  -H "Content-Type: application/json" ^
  -d "{\"login\":\"john@example.com\",\"password\":\"qwerty\"}"
```

Ответ (200):

```json
{
  "access_token": "<ACCESS_TOKEN>",
  "refresh_token": "<REFRESH_TOKEN>",
  "token_type": "bearer"
}
```

Дальше во всех защищённых эндпоинтах используйте заголовок:

```text
Authorization: Bearer <ACCESS_TOKEN>
```

### Поиск пользователя по логину

Запрос:

```bash
curl -s "http://localhost:8000/api/v1/users/by-login/john@example.com" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

Ответ (200):

```json
{
  "id": 1,
  "login": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Поиск пользователя по маске имени и фамилии

Запрос:

```bash
curl -s "http://localhost:8000/api/v1/users/search?mask=jo" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

Ответ (200):

```json
[
  {
    "id": 1,
    "login": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
]
```

### Создание новой цели

Запрос:

```bash
curl -s -X POST "http://localhost:8000/api/v1/goals" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Сдать лабу №2\"}"
```

Ответ (200):

```json
{
  "id": 1,
  "title": "Сдать лр №2",
  "owner_id": 1
}
```

### Получение списка всех целей

Запрос:

```bash
curl -s "http://localhost:8000/api/v1/goals" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

Ответ (200):

```json
[
  {
    "id": 1,
    "title": "Сдать лр №2",
    "owner_id": 1
  }
]
```

### Создание новой задачи на пути к цели

Запрос:

```bash
curl -s -X POST "http://localhost:8000/api/v1/tasks" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"goal_id\":1,\"title\":\"Написать README\",\"status\":\"new\"}"
```

Ответ (200):

```json
{
  "id": 1,
  "goal_id": 1,
  "title": "Написать README",
  "owner_id": 1,
  "status": "new"
}
```

### Получение всех задач цели

Запрос:

```bash
curl -s "http://localhost:8000/api/v1/tasks/by-goal/1" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

Ответ (200):

```json
[
  {
    "id": 1,
    "goal_id": 1,
    "title": "Написать README",
    "owner_id": 1,
    "status": "new"
  }
]
```

### Изменение статуса задачи в цели

Запрос:

```bash
curl -s -X PATCH "http://localhost:8000/api/v1/tasks/1/status" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"status\":\"done\"}"
```

Ответ (200):

```json
{
  "id": 1,
  "goal_id": 1,
  "title": "Написать README",
  "owner_id": 1,
  "status": "done"
}
```
