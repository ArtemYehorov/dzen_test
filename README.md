# 💬 Dzen Test — система комментариев

Этот проект — система комментариев с вложенностью, поддержкой файлов и CAPTCHA. Реализован как тестовое задание на Junior+ Python/Django разработчика. Пользователь указывает имя и email при каждом комментировании — полноценная авторизация не требуется.

## 🔧 Стек технологий

- **Backend**: Django, Django REST Framework, SimpleJWT (только для админов), Celery, Redis
- **Frontend**: Vue 3, Axios, Tailwind CSS
- **БД**: SQLite 
- **Кэш**: Redis
- **DevOps**: Docker, Docker Compose
- **Хостинг**: Render.com

## ✨ Функциональность

- Добавление и отображение комментариев
- Поддержка вложенности (ответы)
- CAPTCHA защита от спама
- Прикрепление изображений и текстовых файлов
- Определение и отображение кодировки файлов
- Просмотр изображений в Lightbox
- Пагинация (по 25 комментариев)
- Сортировка по имени, email и дате
- Выбор родителя для ответа
- Кэширование (3 минуты)
- Полностью Docker-совместим

## 🔗 Демо

- [Frontend (Render)](https://dzen-test-frontend.onrender.com)
- [Backend API (Render)](https://dzen-test-fjvl.onrender.com/api/)

## 🚀 Как запустить проект (шаг за шагом)

### ✅ Шаг 1. Склонируй репозиторий:

```bash
git clone https://github.com/ArtemYehorov/dzen_test.git
cd dzen_test
```

---

### 🐳 Шаг 2. Запуск бэкенда (Django) через Docker

1. Установи [Docker Desktop](https://www.docker.com/products/docker-desktop/) и запусти его.
2. В папке `dzen_test` выполни:

```bash
docker compose up --build
```

⏱ Первый запуск может занять несколько минут — дождись, пока всё соберётся.

Бэк доступен по адресу: [http://localhost:8000/api/](http://localhost:8000/api/)

---

### 🌐 Шаг 3. Запуск фронтенда (Vue)

1. Перейди в папку фронта:

```bash
cd frontend
```

2. Установи зависимости (требуется Node.js, [скачать тут](https://nodejs.org/)):

```bash
npm install
```

3. Запусти фронт:

```bash
npm run dev
```

4. Перейди в браузере по адресу:

[http://localhost:5173](http://localhost:5173)

---

## 📦 Структура проекта

```
dzen_test/
├── comment_project/       # Django-проект
├── comments/              # Приложение комментариев
├── frontend/              # Vue SPA
├── media/                 # Загружаемые файлы
├── docker-compose.yml     # Docker конфигурация
├── Dockerfile             # Dockerfile backend
└── README.md
```

## 🔍 Пример API

Запрос комментариев:
```http
GET /api/comments/?page=1&ordering=-created_at
```

Создание комментария:
```json
{
  "user": {
    "name": "Ivan",
    "email": "ivan@example.com"
  },
  "text": "Тестовый комментарий",
  "captcha": "код",
  "captcha_key": "ключ",
  "file": null,
  "parent": null
}

```
ER-диаграмма MySQL Workbench: [dzen_test_schema.mwb](./dzen_test_schema.mwb)
```
[Artem Yehorov](https://github.com/ArtemYehorov)