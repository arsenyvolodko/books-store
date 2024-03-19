# book-store

## Description

DRF API for a online book store.

## Common

Проект задеплойен на сервере по адресу: http://154.194.53.151:9500

SWAGGER: http://154.194.53.151:9500/swagger/

## Admin panel

Админ панель доступна по адресу: http://154.194.53.151:9500/admin/
Данные для авторизации:

- username: root
- password: 1111

## Installation

Для локального развертывания проекта необходимо выполнить следующие шаги:

```bash
poetry shell
poetry lock
poetry install --no-root
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

## API endpoints

Подробная информация о всех эндпоинтах доступна в [Swagger](http://154.194.53.151:9500/swagger/). Здесь представлено
краткое дополнительное описание.\
Для использования API необходимо авторизоваться.
Для авторизации необходимо отправить POST запрос на ```http://154.194.53.151:9500/signup/``` с данными:

```json
{
  "username": "username",
  "password": "password"
}
```

Можно также авторизоваться через [Swagger](http://154.194.53.151:9500/swagger/).\
В случае успешной авторизации сервер вернет токен, который необходимо использовать для обращения к API.
При использовании [Swagger](http://154.194.53.151:9500/swagger/) в поле авторизации необходимо указать токен в формате "
Token [token]", где [token] - токен, полученный при авторизации.

1. `http://154.194.53.151:9500/books/get_book/{book_id}` - получение информации о книге по id
2. `http://154.194.53.151:9500/books/get_books/` - получение списка книг категории (пагинация по 50 книг), см. опциональные параметры (фильтры) в [Swagger](http://154.194.53.151:9500/swagger/)
3. `http://154.194.53.151:9500/books/get_cats_and_books?category=Java` - получение списка книг заданной категории (Java),
   подкатегорий заданной категории, а также книг данных подкатегорий
4. `http://154.194.53.151:9500/books/feedback/` - форма обратной связи

## Добавление подкатегорий

Для добавления подкатегорий через панель админа необходимо открыть таблицу `Category hierarchys` и добавить новую связь
категории и подкатегории.
При добавлении предусмотрена проверка на то, что
   - подкатегория и категория не могут быть одинаковыми
   - у подкатегории уже нет родительской категории
   - не образуется цикл, гарантируется древовидная структура
