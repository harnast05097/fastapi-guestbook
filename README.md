# Гостевая книга на FastAPI
## Установка и запуск

Нужен Python 3.11 или новее. Выполняйте команды из папки `fastapi-guestbook`, рядом с `main.py`.

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

**macOS и Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m alembic upgrade head
python -m uvicorn main:app --reload
```

Перед первым запуском приложения обязательно выполните `alembic upgrade head`. После запуска откройте [Swagger UI](http://127.0.0.1:8000/docs). Данные сохраняются в SQLite и остаются после перезапуска сервера.

## API

| Метод и путь                  | Назначение | Успешный ответ |
|-------------------------------| --- | --- |
| `POST /reviews`               | Создать отзыв | `201`, созданный отзыв |
| `GET /reviews`                | Получить список, новые отзывы сверху | `200`, массив отзывов |
| `GET /reviews?author=Настя`   | Фильтр по имени автора | `200`, массив отзывов |
| `GET /reviews/{review_id}`    | Получить один отзыв | `200`, отзыв |
| `DELETE /reviews/{review_id}` | Удалить отзыв | `204`, пустое тело |

Тело запроса для `POST /reviews`:

```json
{
  "author": "Настя",
  "text": "Круто!"
}
```

Автор после удаления пробелов по краям должен содержать от 1 до 80 символов, текст — от 1 до 1000. Пустые строки и строки только из пробелов отклоняются с `422`. `GET` и `DELETE` для несуществующего отзыва отвечают `404`; ID должен быть положительным числом.

## Тесты
Из папки с main.py, в том же окружении:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -v
```

