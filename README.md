# Wildberries Product Parser

Парсер для сбора данных о товарах с сайта Wildberries. Реализован с использованием Django и Selenium. Сохраняет результаты в базу данных.

## Возможности

- Поиск товаров по ключевому слову
- Сбор данных с нескольких страниц поиска
- Извлечение информации:
  - Название товара
  - Цена со скидкой
  - Старая цена (если есть)
  - Рейтинг
  - Количество отзывов

## Установка

1. Клонируйте проект и перейдите в его папку.
2. - virtualenv virt
- cd virt
- cd Scripts
- cd activate
3. Установите зависимости:
pip install -r requirements.txt

4. Выполните миграции базы данных:
- python manage.py makemigrations
- python manage.py migrate

## Использование

Запуск парсера:
- python manage.py parse_wb <ключевое_слово> --pages=<количество_страниц>

Пример:
- python manage.py parse_wb смартфон --pages=2
- python manage.py runserver
- Просмотр API /api/products

## Зависимости

Используемые библиотеки:
- Django
- selenium
- webdriver-manager
- requests
- beautifulsoup4
