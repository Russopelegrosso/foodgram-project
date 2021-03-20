# Foodgram
### Описание
Онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд

The site is available on http://178.154.210.199


## Стек технологий
- Python 3.8
- Django and Django Rest Framework
- PostgreSQL
- Gunicorn + Nginx
- CI/CD: Docker, docker-compose, GitHub Actions
- Yandex.Cloud

## Как запустить проект
- Клонируйте репозитроий с проектом:
    ```
    git clone https://github.com/Russopelegrosso/foodgram-project.git
    ```
- Перейдите в директорию проекта
    ```
    cd foodgram-project/
    ```
- Запустите docker-compose
    ```
    docker-compose -f docker-compose.yaml up -d
    ```
- В новом окне терминала узнайте id контейнера foodgram и войдите в контейнер:
    ```
    docker container ps
    docker exec -it <CONTAINER_ID> bash
    ```
- В контейнере выполните migrate, создайте createsuperuser и collectstatic:
    ```
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py collectstatic
    ```