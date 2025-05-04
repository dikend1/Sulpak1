![image](https://github.com/user-attachments/assets/3f879478-67f3-43a2-8fe6-b51b1ebcab52)﻿# Проект для хакатона: Система заказов ресторана

## Описание

Repository Frontend = https://github.com/tortugichh/koshpendi-menu

Это проект для хакатона, в котором мы создаем платформу для управления заказами ресторанов. В проекте реализованы следующие функции:

- Регистрация и авторизация пользователей (клиентов и ресторанов).
- Управление меню ресторана (добавление, редактирование, удаление блюд).
- Система заказов с возможностью добавления блюд в заказ.
- Просмотр отзывов для ресторанов.
- Система рейтингов для блюд и ресторанов.
  
Проект использует **Django** для бэкенда, **React** для фронтенда, **PostgreSQL** для хранения данных, а также задеплоен на **Railway** и **Vercel** для продакшн-среды.

## Стек технологий

- **Backend:** Django (Python)
- **Frontend:** React.js
- **Database:** PostgreSQL
- **Deployment:** Railway (для бэкенда), Vercel (для фронтенда)
- **API Documentation:** Swagger UI
- **Version Control:** Git, GitHub

## Установка и запуск

### Для разработки

1. **Клонировать репозиторий:**

    ```bash
    git clone https://github.com/dikend1/Sulpak1.git
    cd Sulpak1
    ```

2. **Установить виртуальное окружение для Django:**

    Для Python 3.10+ используйте следующие команды:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Для Linux/macOS
    .venv\Scripts\activate     # Для Windows
    ```

3. **Установить зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Настройка базы данных:**

    Убедитесь, что у вас установлен PostgreSQL и настроена база данных. Выполните миграции:

    ```bash
    python manage.py migrate
    ```

5. **Создание суперпользователя (для админ панели):**

    ```bash
    python manage.py createsuperuser
    ```

6. **Запуск проекта:**

    Запустите сервер Django:

    ```bash
    python manage.py runserver
    ```

    Приложение будет доступно по адресу: `http://127.0.0.1:8000`

7. **Запуск фронтенда:**

    Перейдите в директорию `frontend`:

    ```bash
    cd frontend
    ```

    Установите зависимости:

    ```bash
    npm install
    ```

    Запустите приложение:

    ```bash
    npm start
    ```

    Приложение будет доступно по адресу: `http://localhost:3000`

### Для продакшн-среды

1. **Деплой на Railway (для бэкенда):**

    - Перейдите в [Railway](https://railway.app/) и создайте новый проект.
    - Подключите ваш репозиторий GitHub.
    - Укажите переменные окружения для подключения к базе данных (например, `DATABASE_URL`).

2. **Деплой на Vercel (для фронтенда):**

    - Перейдите в [Vercel](https://vercel.com/) и создайте новый проект.
    - Подключите ваш репозиторий GitHub.
    - Разверните приложение и получите публичный URL.

## API Endpoints

### 1. **Регистрация и авторизация**

- `POST /api/register/` — Регистрация нового пользователя.
- `POST /api/login/` — Авторизация пользователя.

### 2. **Меню ресторана**

- `GET /api/menu/<int:restaurant_id>/` — Получить меню ресторана.
- `POST /api/menu/<int:restaurant_id>/add_dish/` — Добавить новое блюдо в меню.
- `PATCH /api/menu/<int:restaurant_id>/edit_dish/<int:dish_id>/` — Редактировать блюдо.
- `DELETE /api/menu/<int:restaurant_id>/delete_dish/<int:dish_id>/` — Удалить блюдо.

### 3. **Заказы**

- `GET /api/orders/` — Получить все заказы.
- `GET /api/orders/<int:order_id>/` — Получить заказ по ID.
- `POST /api/orders/add_order/` — Создать новый заказ.
- `GET /api/orders/customer/<int:customer_id>/` — Получить заказы по ID клиента.
- `GET /api/orders/restaurant/<int:restaurant_id>/` — Получить заказы по ID ресторана.

### 4. **Отзывы**

- `POST /api/review/<int:restaurant_id>/` — Оставить отзыв для ресторана.
- `GET /api/reviews/<int:restaurant_id>/` — Получить все отзывы для ресторана.

## Пример использования API через Postman

### Пример запроса на создание заказа:
**Метод:** `POST`  
**URL:** `http://127.0.0.1:8000/api/orders/add_order/`  
**Тело запроса (Body):**

```json
{
  "restaurant": 1,
  "dishes": [1, 2, 3],
  "total_price": 100.50,
  "user_number": "1234567890",
  "order_status": "Cooking"
}
