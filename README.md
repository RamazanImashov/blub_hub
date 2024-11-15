# Документация для BlubHub

## 1. Общая информация о проекте

**Название проекта:** BlubHub  
**Описание:**  
BlubHub — это платформа для обмена видео, аналогичная YouTube, которая позволяет пользователям регистрироваться, загружать видео, подписываться на других пользователей и взаимодействовать через комментарии, лайки, дизлайки и рейтинги. Проект демонстрирует широкий спектр функций видеоплатформы, включая аутентификацию пользователей, управление медиа и гибкое API.

---

## 2. Стек технологий

- **Бэкенд:** Django с Django Rest Framework (DRF)
- **Аутентификация:** JWT (токены JSON Web)
- **Очередь задач:** Celery для асинхронных задач (например, уведомления по электронной почте)
- **База данных:** PostgreSQL
- **Кэширование и очереди сообщений:** Redis
- **Дополнительные интеграции:** Почтовый сервис для уведомлений при регистрации и восстановлении пароля

---

## 3. Структура проекта

```plaintext
.
├── README.md
├── account/                    # Управление аккаунтами пользователей
│   ├── models.py               # Модели пользователей с уникальными полями и методами
│   ├── serializers.py          # DRF-сериализаторы для обработки ввода и вывода данных пользователей
│   ├── tasks.py                # Задачи Celery для уведомлений по почте
│   ├── views.py                # Представления DRF для регистрации, входа, выхода и т.д.
│   └── urls.py                 # URL-адреса для работы с аккаунтами
├── apps/                       # Основные функции BlubHub
│   ├── review/                 # Комментарии, рейтинги, лайки/дизлайки
│   │   ├── models.py           # Модели комментариев, лайков, дизлайков, рейтингов
│   │   ├── serializers.py      # Сериализаторы DRF для функций отзывов
│   │   ├── views.py            # Представления DRF для обработки отзывов
│   │   └── urls.py             # URL-адреса для отзывов
│   └── video/                  # Управление видео
│       ├── models.py           # Модели видео и тем
│       ├── serializers.py      # Сериализаторы DRF для функций работы с видео
│       ├── views.py            # Представления DRF для загрузки видео и взаимодействия
│       └── urls.py             # URL-адреса для видео
├── config/                     # Настройки Django и конфигурации Celery
│   ├── settings.py             # Основные настройки Django
│   ├── celery.py               # Конфигурация Celery для асинхронных задач
│   ├── urls.py                 # Основной URL-роутинг
│   └── wsgi.py                 # Точка входа WSGI
└── requirements.txt            # Зависимости проекта
```

---

## 4. Установка

1. **Установите зависимости**:
   - Python 3.11
   - PostgreSQL

2. **Настройка проекта**:
   - **Виртуальная среда**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```
   - **Настройка базы данных**:
     - Убедитесь, что PostgreSQL запущен.
     - Создайте базу данных и пользователя:
       ```sql
       CREATE DATABASE blubhub;
       CREATE USER blubhub_user WITH PASSWORD 'password';
       ```
   - **Переменные окружения**:
     Создайте файл `.env` в корневой директории со следующими переменными:
     ```env
     DEBUG=False
     DB_NAME=blubhub
     DB_USER=blubhub_user
     DB_PASS=password
     DB_HOST=localhost
     EMAIL_HOST_USER=email@example.com
     EMAIL_HOST_PASSWORD=email_password
     ```
   - **Миграции**:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

3. **Запуск сервера**:
   ```bash
   python manage.py runserver
   ```

---

## 5. Основные функции и API эндпоинты

### 5.1 Управление аккаунтами (`/account/`)

- **Эндпоинты**:
  - `POST /register/`: Регистрация нового пользователя с подтверждением по электронной почте.
  - `GET /activate/<str:email>/<str:activation_code>/`: Активация аккаунта.
  - `POST /login/`: Получение JWT токенов.
  - `POST /logout/`: Выход с помощью добавления JWT в черный список.
  - `POST /change_password/`: Смена пароля.
  - `POST /lose_password/`: Запрос на сброс пароля.
  - `POST /lose_confirm/`: Завершение сброса пароля.

### 5.2 Управление видео (`/video/`)

- **Эндпоинты**:
  - `POST /videos/`: Загрузка нового видео.
  - `GET /videos/`: Список всех видео с возможностью фильтрации.
  - `GET /videos/<slug>/`: Просмотр детальной информации о видео.
  - `POST /videos/<slug>/like/`: Лайкнуть видео.
  - `POST /videos/<slug>/dislike/`: Дизлайкнуть видео.
  - `POST /videos/<slug>/watch_later/`: Добавить видео в «смотреть позже».
  - `POST /videos/<slug>/comments/`: Добавить комментарий к видео.
  - `POST /videos/<slug>/rating/`: Добавить или обновить рейтинг.

### 5.3 Управление отзывами (`/review/`)

- **Эндпоинты**:
  - `POST /comments/`: Добавить новый комментарий.
  - `GET /comments/`: Список комментариев к видео.
  - `POST /likes/`: Лайк к видео.
  - `POST /dislikes/`: Дизлайк к видео.
  - `POST /ratings/`: Оценка видео.

---

## 6. Разрешения

- **AllowAny**: Доступ для всех пользователей (например, просмотр видео и комментариев).
- **IsAuthenticated**: Требуется для взаимодействия с контентом (например, лайк, комментарии).
- **IsAdminUser**: Доступ только для администраторов.
- **IsAuthorPermission**: Проверка, что только автор может обновлять или удалять свой контент.

---

## 7. Задачи Celery и фоновая обработка

Celery используется для обработки асинхронных задач, особенно для отправки писем. Эти задачи определены в `tasks.py` в приложении `account`.

- **Письмо для активации**: Отправляется новым пользователям при регистрации.
- **Письмо для сброса пароля**: Отправляется при запросе на восстановление пароля.

### Запуск Celery

Чтобы запустить Celery, используйте:
```bash
celery -A config worker -l info
```

---

## 8. Будущие улучшения

- **Поддержка потокового воспроизведения**: Оптимизация платформы для потокового видео.
- **Расширенный поиск**: Улучшение поиска с возможностью фильтрации.
- **Рекомендательная система**: Предложение видео на основе истории просмотров.
- **Уведомления**: Встроенные уведомления и письма при новых комментариях, лайках и подписках.

---

Эта документация предоставляет базовое понимание структуры проекта BlubHub, настройки, основных функций и будущих планов. Настройки можно корректировать в зависимости от среды или требований к развертыванию.
