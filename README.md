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

## Хранилище

Все сервисы используют in-memory хранилище в рамках контейнера.

## Запуск

```bash
docker compose up --build
```

Прокси доступен на `http://localhost:8000`.
Swagger прокси: `http://localhost:8000/docs`.

## Если Docker не может скачать пакеты напрямую

В `Dockerfile` для сервисов зависимости ставятся без доступа к сети:
- `pip install --no-index --find-links /wheels -r requirements.txt`
- контейнер берет prebuilt wheels из папки `wheelhouse_linux/`

Если при `docker compose up --build` падает установка пакетов (ошибки сети/прокси/доступа к PyPI), нужно заранее докачать wheel'ы на хост и положить их в `wheelhouse_linux/`.

### Шаги (Windows / PowerShell)

1. Перейдите в папку `lab_2`:
```powershell
cd lab_2
```

2. Скачайте Linux wheels (для `python:3.12-slim`) во `wheelhouse_linux`:
```powershell
$dest = "wheelhouse_linux"
New-Item -ItemType Directory -Force $dest | Out-Null

$platform = "manylinux_2_17_x86_64"
$pythonVersion = "3.12"
$implementation = "cp"
$abi = "cp312"

$reqFiles = Get-ChildItem -Path backend -Directory -Filter "*_service" |
  ForEach-Object { Join-Path $_.FullName "requirements.txt" }

foreach ($rf in $reqFiles) {
  pip download `
    --dest $dest `
    --platform $platform `
    --python-version $pythonVersion `
    --implementation $implementation `
    --abi $abi `
    --only-binary=:all: `
    -r $rf
}
```

3. Убедитесь, что папка `wheelhouse_linux` заполнена `.whl` файлами.

4. Запустите сборку заново:
```powershell
docker compose up --build
```

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
