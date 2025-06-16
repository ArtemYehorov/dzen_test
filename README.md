# 💬 Dzen Test — система комментариев

Этот проект представляет собой полнофункциональную систему комментариев с поддержкой вложенности, файлов, изображений и CAPTCHA. Он реализован в рамках тестового задания на позицию Junior+ Python/Django разработчика.

## 🔧 Стек технологий

- Backend: **Django**, **Django REST Framework**, **SimpleJWT**, **Celery**, **Redis**
- Frontend: **Vue 3**, **Axios**, **Tailwind CSS**
- База данных: **SQLite**
- Кэш: **Redis**
- Контейнеризация: **Docker**, **Docker Compose**
- CI/CD и хостинг: **Render.com**

## ✨ Возможности

- Регистрация пользователей
- Создание, отображение и вложенность комментариев
- Валидация через **CAPTCHA**
- Поддержка **изображений и текстовых файлов**
- Просмотр изображений через **Lightbox**
- Автоматическое определение и отображение кодировки текстовых файлов
- Сортировка заглавных комментариев по имени, email и дате
- Пагинация (по 25 комментариев)
- Возможность выбора родителя комментария
- Кэширование запросов (3 минуты)
- Интернационализация (многоязычность возможна)
- Dockerized и готов к деплою на Render

## 🚀 Демо

- 🔗 [Backend (Render)](https://dzen-test-fjvl.onrender.com/api)
- 🔗 [Frontend (Render)](https://dzen-test-frontend.onrender.com)

## 🐳 Запуск в Docker

```bash
git clone https://github.com/ArtemYehorov/dzen_test.git
cd dzen_test
docker-compose up --build
```

## 🧪 Пример API запроса

Получить список комментариев:
```
GET /api/comments/?page=1&ordering=-created_at
```

Создание комментария (POST /api/comments/):
```json
{
  "user": {
    "name": "Artem",
    "email": "artem@example.com"
  },
  "text": "Комментарий",
  "captcha": "1234",
  "captcha_key": "abc123",
  "file": null,
  "parent": null
}
```

## 🗃 Структура проекта

- `comment_project/` — основной Django-проект
- `comments/` — приложение с логикой комментариев
- `frontend/` — Vue SPA
- `media/` — директория для загруженных файлов

## 📄 Лицензия

MIT

---
Проект выполнил [Artem Yehorov](https://github.com/ArtemYehorov)
